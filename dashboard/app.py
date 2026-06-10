import os
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st
from sqlalchemy import create_engine


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


@st.cache_data(ttl=60)
def load_data() -> tuple[pd.DataFrame, str]:
    try:
        engine = create_engine(database_url(), pool_pre_ping=True)
        customers = pd.read_sql("select * from analytics.stg_customers", engine)
        return customers, "warehouse"
    except Exception:
        customers = pd.read_csv(CSV_PATH, comment="#")
        customers["signup_date"] = pd.to_datetime(customers["signup_date"])
        return customers, "demo CSV"


st.set_page_config(page_title="Analytics Intelligence Platform", layout="wide")
st.title("Analytics Intelligence Platform")

customers, source = load_data()
customers["signup_date"] = pd.to_datetime(customers["signup_date"])
customers["monthly_revenue"] = pd.to_numeric(customers["monthly_revenue"])
customers["status"] = customers["status"].str.lower()

total_revenue = customers["monthly_revenue"].sum()
total_customers = len(customers)
active_customers = int((customers["status"] == "active").sum())
churn_rate = float((customers["status"] == "churned").sum() / total_customers) if total_customers else 0.0

st.caption(f"Data source: {source}")
metric_cols = st.columns(4)
metric_cols[0].metric("Total Revenue", f"${total_revenue:,.0f}")
metric_cols[1].metric("Total Customers", f"{total_customers:,}")
metric_cols[2].metric("Active Customers", f"{active_customers:,}")
metric_cols[3].metric("Churn Rate", f"{churn_rate:.1%}")

monthly = (
    customers.assign(signup_month=customers["signup_date"].dt.to_period("M").dt.to_timestamp())
    .groupby("signup_month", as_index=False)
    .agg(total_revenue=("monthly_revenue", "sum"), customers=("customer_id", "count"))
)

left, right = st.columns(2)
with left:
    st.plotly_chart(
        px.line(monthly, x="signup_month", y="total_revenue", markers=True, title="Revenue by Signup Month"),
        use_container_width=True,
    )
with right:
    st.plotly_chart(
        px.bar(monthly, x="signup_month", y="customers", title="Customer Growth"),
        use_container_width=True,
    )

country_counts = customers.groupby("country", as_index=False).agg(customers=("customer_id", "count"))
st.plotly_chart(
    px.pie(country_counts, names="country", values="customers", title="Country Distribution"),
    use_container_width=True,
)
