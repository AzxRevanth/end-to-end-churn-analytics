import pandas as pd
import os 
from sqlalchemy import create_engine
import numpy as np
import psycopg2
from dotenv import load_dotenv
from pathlib import Path
from datetime import date
from dateutil.relativedelta import relativedelta

ROOT_DIR = Path(__file__).resolve().parents[1]
ENV_PATH = ROOT_DIR / ".env"

load_dotenv(dotenv_path=ENV_PATH)

conn = psycopg2.connect(
    host=os.getenv("PG_HOST"),
    database=os.getenv("PG_DB"),
    user=os.getenv("PG_USER"),
    password=os.getenv("PG_PASSWORD"),
    port=5432
)

engine = create_engine(
    f"postgresql+psycopg2://{os.getenv('PG_USER')}:{os.getenv('PG_PASSWORD')}"
    f"@{os.getenv('PG_HOST')}:{os.getenv('PG_PORT', '5432')}/{os.getenv('PG_DB')}",
    pool_pre_ping=True,
    pool_recycle=300
)

# MONTH 1
# query = "SELECT * FROM customer_monthly_snapshot"
# df = pd.read_sql(query, con=engine)
# # print(df)
# snapshot_date = date(2026, 1, 1)
# df['snapshot_month'] = snapshot_date
# df.to_sql(
#     name="customer_monthly_snapshot",
#     con=engine,
#     if_exists="replace",
#     index=False
# )
# print("Month 1 snapshot inserted successfully")


TABLE_NAME = "customer_monthly_snapshot"
def get_latest_snapshot():
    query = f"""
        SELECT *
        FROM {TABLE_NAME}
        WHERE snapshot_month = (
            SELECT MAX(snapshot_month) FROM {TABLE_NAME}
        )
    """
    return pd.read_sql(query, engine)

def get_next_month(latest_month):
    return (latest_month + relativedelta(months=1)).replace(day=1)

def simulate(df):
    df_new = df.copy()

    df_new["tenure"] = df_new["tenure"] + 1
    df_new["total_charges"] = df_new["total_charges"] + df_new["monthly_charges"]

    df_new["monthly_charges"] = df_new["monthly_charges"] * (
        1 + np.random.normal(0, 0.02, len(df_new))
    )

    return df_new

# ---- MAIN ----
def main():
    df_latest = get_latest_snapshot()

    latest_month = pd.to_datetime(df_latest["snapshot_month"].iloc[0]).date()
    next_month = get_next_month(latest_month)

    print(f"Simulating data for {next_month}")

    sim_df = simulate(df_latest)
    sim_df["snapshot_month"] = next_month

    sim_df.to_sql(
        name=TABLE_NAME,
        con=engine,
        if_exists="append",
        index=False
    )

    print("Simulation completed successfully")

if __name__ == "__main__":
    main()