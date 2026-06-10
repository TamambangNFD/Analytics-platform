from __future__ import annotations

from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator


DEFAULT_ARGS = {
    "owner": "data-platform",
    "depends_on_past": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="daily_analytics_pipeline",
    description="Ingest, validate, transform, and publish analytics data.",
    default_args=DEFAULT_ARGS,
    start_date=datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["analytics-platform"],
) as dag:
    ingest_customers = BashOperator(
        task_id="ingest_customers",
        bash_command="python /opt/airflow/pipelines/ingestion.py",
    )

    run_quality_checks = BashOperator(
        task_id="run_quality_checks",
        bash_command="python /opt/airflow/quality/checks.py",
    )

    run_dbt_transformations = BashOperator(
        task_id="run_dbt_transformations",
        bash_command="dbt run --project-dir /opt/airflow/dbt --profiles-dir /opt/airflow/dbt",
    )

    test_dbt_models = BashOperator(
        task_id="test_dbt_models",
        bash_command="dbt test --project-dir /opt/airflow/dbt --profiles-dir /opt/airflow/dbt",
    )

    refresh_dashboard = EmptyOperator(task_id="refresh_dashboard_placeholder")

    ingest_customers >> run_quality_checks >> run_dbt_transformations >> test_dbt_models >> refresh_dashboard
