import logging
import os
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text


EXPECTED_COLUMNS = [
    "customer_id",
    "customer_name",
    "email",
    "country",
    "signup_date",
    "subscription_plan",
    "monthly_revenue",
    "status",
]

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "pipelines" / "data" / "customers.csv"


def database_url() -> str:
    user = os.getenv("DATABASE_USER", "demo_user")
    password = os.getenv("DATABASE_PASSWORD", "demo_password")
    host = os.getenv("DATABASE_HOST", "localhost")
    port = os.getenv("DATABASE_PORT", "5432")
    name = os.getenv("DATABASE_NAME", "analytics")
    return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{name}"


def load_customers(path: Path = DATA_PATH) -> pd.DataFrame:
    logging.info("Loading %s", path.name)
    df = pd.read_csv(path, comment="#")
    missing = sorted(set(EXPECTED_COLUMNS) - set(df.columns))
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}")

    df = df[EXPECTED_COLUMNS].copy()
    df["customer_id"] = pd.to_numeric(df["customer_id"], errors="raise").astype("int64")
    df["customer_name"] = df["customer_name"].fillna("Unknown Customer").str.strip()
    df["email"] = df["email"].fillna("unknown@example.com").str.lower().str.strip()
    df["country"] = df["country"].fillna("Unknown").str.strip()
    df["subscription_plan"] = df["subscription_plan"].fillna("Free").str.strip()
    df["status"] = df["status"].fillna("unknown").str.lower().str.strip()
    df["monthly_revenue"] = pd.to_numeric(df["monthly_revenue"], errors="coerce").fillna(0.0)
    df["signup_date"] = pd.to_datetime(df["signup_date"], errors="raise").dt.date
    return df


def load_to_postgres(df: pd.DataFrame) -> None:
    engine = create_engine(database_url(), pool_pre_ping=True)
    with engine.begin() as conn:
        conn.execute(text("create schema if not exists raw"))
        conn.execute(text("create schema if not exists analytics"))
        df.to_sql("customers", conn, schema="raw", if_exists="replace", index=False)
        conn.execute(text("alter table raw.customers add primary key (customer_id)"))


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    try:
        df = load_customers()
        load_to_postgres(df)
        logging.info("Records processed: %s", len(df))
        logging.info("Status: SUCCESS")
    except Exception:
        logging.exception("Status: FAILED")
        raise


if __name__ == "__main__":
    main()
