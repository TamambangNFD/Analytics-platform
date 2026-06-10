import logging
import os
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text


EXPECTED_COLUMNS = {
    "customer_id",
    "customer_name",
    "email",
    "country",
    "signup_date",
    "subscription_plan",
    "monthly_revenue",
    "status",
}

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "pipelines" / "data" / "customers.csv"


def database_url() -> str:
    return (
        f"postgresql+psycopg2://{os.getenv('DATABASE_USER', 'demo_user')}:"
        f"{os.getenv('DATABASE_PASSWORD', 'demo_password')}@"
        f"{os.getenv('DATABASE_HOST', 'localhost')}:"
        f"{os.getenv('DATABASE_PORT', '5432')}/"
        f"{os.getenv('DATABASE_NAME', 'analytics')}"
    )


def load_customers() -> pd.DataFrame:
    try:
        engine = create_engine(database_url(), pool_pre_ping=True)
        return pd.read_sql("select * from raw.customers", engine)
    except Exception:
        logging.warning("Database unavailable; running quality checks against demo CSV.")
        return pd.read_csv(CSV_PATH, comment="#")


def run_checks(df: pd.DataFrame) -> list[str]:
    failures: list[str] = []
    missing_columns = EXPECTED_COLUMNS - set(df.columns)
    if missing_columns:
        failures.append(f"Missing columns: {', '.join(sorted(missing_columns))}")
        return failures

    if df["customer_id"].isna().any():
        failures.append("customer_id cannot be null")
    if df["customer_id"].duplicated().any():
        failures.append("customer_id must be unique")
    if df[["customer_name", "email", "country", "signup_date", "subscription_plan", "status"]].isna().any().any():
        failures.append("Required descriptive fields cannot be null")
    if pd.to_numeric(df["monthly_revenue"], errors="coerce").isna().any():
        failures.append("monthly_revenue must be numeric")
    if (pd.to_numeric(df["monthly_revenue"], errors="coerce") < 0).any():
        failures.append("monthly_revenue >= 0")
    return failures


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    df = load_customers()
    failures = run_checks(df)
    if failures:
        for failure in failures:
            logging.error(failure)
        raise SystemExit("Data quality checks failed")
    logging.info("Data quality checks: SUCCESS")


if __name__ == "__main__":
    main()
