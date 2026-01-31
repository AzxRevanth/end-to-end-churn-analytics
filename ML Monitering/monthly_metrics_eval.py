import pandas as pd
import os
from sqlalchemy import create_engine
from scipy.stats import spearmanr
from datetime import date
from dotenv import load_dotenv
from pathlib import Path

# env
ROOT_DIR = Path(__file__).resolve().parents[1]
ENV_PATH = ROOT_DIR / ".env"
load_dotenv(ENV_PATH)

engine = create_engine(
    f"postgresql+psycopg2://{os.getenv('PG_USER')}:{os.getenv('PG_PASSWORD')}"
    f"@{os.getenv('PG_HOST')}:{os.getenv('PG_PORT', '5432')}/{os.getenv('PG_DB')}",
    pool_pre_ping=True
)

def load_preds(month, model):
    q = f"""
        SELECT customer_id, churn_probability, retention_priority_score
        FROM monthly_churn_predictions
        WHERE snapshot_month = '{month}'
          AND model_name = '{model}'
    """
    return pd.read_sql(q, engine)

def compute_metrics(df_curr, df_prev=None):
    avg_churn = df_curr["churn_probability"].mean()
    high_risk_pct = (df_curr["churn_probability"] >= 0.6).mean()
    revenue_at_risk = df_curr["retention_priority_score"].sum()

    if df_prev is not None:
        merged = df_curr.merge(df_prev, on="customer_id", suffixes=("_c", "_p"))
        rank_stability = spearmanr(
            merged["churn_probability_c"],
            merged["churn_probability_p"]
        )[0]
    else:
        rank_stability = None
    
    return avg_churn, high_risk_pct, revenue_at_risk, rank_stability

def main(run_month):
    prev_month = (pd.to_datetime(run_month) - pd.DateOffset(months=1)).date()

    rows = []

    for model in ["logreg", "rf"]:
        curr = load_preds(run_month, model)
        prev = load_preds(prev_month, model) if prev_month else None

        metrics = compute_metrics(curr, prev)

        rows.append({
            "snapshot_month": run_month,
            "model_name": model,
            "avg_churn_probability": metrics[0],
            "high_risk_pct": metrics[1],
            "revenue_at_risk": metrics[2],
            "rank_stability_score": metrics[3]
        })

    pd.DataFrame(rows).to_sql(
        "model_snapshot_metrics",
        con=engine,
        if_exists="append",
        index=False
    )

if __name__ == "__main__":
    main(date(2026, 2, 1))
