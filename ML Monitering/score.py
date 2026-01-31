import joblib
import pandas as pd
import os
from sqlalchemy import create_engine
from datetime import date
from pathlib import Path
from dotenv import load_dotenv


ROOT_DIR = Path(__file__).resolve().parents[1]
ENV_PATH = ROOT_DIR / ".env"
load_dotenv(ENV_PATH)

engine = create_engine(
    f"postgresql+psycopg2://{os.getenv('PG_USER')}:{os.getenv('PG_PASSWORD')}"
    f"@{os.getenv('PG_HOST')}:{os.getenv('PG_PORT', '5432')}/{os.getenv('PG_DB')}",
    pool_pre_ping=True
)

MODEL_DIR = "models/"


def load_models():
    logreg = joblib.load(f"{MODEL_DIR}/logistic_regression_model.pkl")
    rf = joblib.load(f"{MODEL_DIR}/random_forest_model.pkl")
    scaler = joblib.load(f"{MODEL_DIR}/scaler.pkl")
    return logreg, rf, scaler

def load_monthly_data(run_month):
    query = f"""
        SELECT *
        FROM customer_monthly_snapshot
        WHERE snapshot_month = '{run_month}'
    """
    return pd.read_sql(query, con=engine)


def score_model(df, X, model, run_month, model_name):
    proba = model.predict_proba(X)[:, 1]

    return pd.DataFrame({
        "customer_id": df["customer_id"],
        "snapshot_month": run_month,
        "model_name": model_name,
        "churn_probability": proba,
        "retention_priority_score": proba * df["monthly_charges"]
    })

def write_predictions(df):
    df.to_sql(
        "monthly_churn_predictions",
        con=engine,
        if_exists="append",
        index=False
    )
    print("Predictions written successfully")


def add_engineered_features(df):
    df = df.copy()

    # tenure based
    df["is_new_customer"] = (df["tenure"] <= 6).astype(int)
    df["is_long_tenure"] = (df["tenure"] >= 24).astype(int)

    # pricing
    avg_charge = df["monthly_charges"].mean()
    df["above_avg_charge"] = (df["monthly_charges"] > avg_charge).astype(int)

    auto_pay_cols = [
        "payment_method_Credit card (automatic)",
        "payment_method_Bank transfer (automatic)"
    ]

    df["is_auto_payment"] = (
        df[auto_pay_cols].sum(axis=1).clip(0, 1)
        if all(col in df.columns for col in auto_pay_cols)
        else 0
    )

    # interactions
    df["price_tenure_interaction"] = df["monthly_charges"] * df["tenure"]
    df["total_charges_tenure_ratio"] = (
        df["total_charges"] / (df["tenure"] + 1)
    )

    # tenure buckets (one-hot, matching training)
    df["tenure_bucket_0-6"] = ((df["tenure"] >= 0) & (df["tenure"] <= 6)).astype(int)
    df["tenure_bucket_6-12"] = ((df["tenure"] >= 7) & (df["tenure"] <= 12)).astype(int)
    df["tenure_bucket_13-24"] = ((df["tenure"] >= 13) & (df["tenure"] <= 24)).astype(int)
    df["tenure_bucket_25-48"] = ((df["tenure"] >= 25) & (df["tenure"] <= 48)).astype(int)
    df["tenure_bucket_49+"] = (df["tenure"] >= 49).astype(int)
    return df

def main(run_month):
    df = load_monthly_data(run_month)

    logreg, rf, scaler = load_models()

    df_feat = add_engineered_features(df)

    X = df_feat.drop(
        columns=[
            "customer_id",
            "snapshot_month",
            "churn",
            "created_at"
        ],
        errors="ignore"
    )

    X = X[scaler.feature_names_in_]
    X_scaled = scaler.transform(X)

    logreg_preds = score_model(df, X_scaled, logreg, run_month, "logreg")
    rf_preds = score_model(df, X_scaled, rf, run_month, "rf")

    final_preds = pd.concat([logreg_preds, rf_preds], axis=0)

    write_predictions(final_preds)

if __name__ == "__main__":
    main(date(2026, 2, 1))
