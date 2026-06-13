# Analytics Platform

A GitHub-ready production-style analytics platform demo for data engineering, analytics engineering, dashboarding, orchestration, monitoring, and AI-ready analytics workflows.

## Architecture

```text
Data Sources
    |
Ingestion Layer: Python pipelines / future Airbyte connectors
    |
Raw Data Layer: PostgreSQL raw schema / BigQuery compatible
    |
Transformation Layer: dbt
    |
Analytics Layer: analytics schema
    |
Dashboard + AI Assistant
```

## Technology Stack

- PostgreSQL for the local warehouse simulation
- Python and pandas for ingestion and validation
- dbt for transformations and tests
- Airflow for orchestration
- Streamlit and Plotly for dashboards
- Rule-based AI assistant as a future LLM integration placeholder
- Docker Compose for local execution

## Repository Layout

```text
analytics-platform/
  architecture/
  pipelines/
  dbt/
  airflow/
  dashboard/
  ai/
  quality/
  docs/
```

## Installation

```bash
git clone <your-repo-url>
cd analytics-platform
cp .env.example .env
docker compose up
```

Dashboard: http://localhost:8501

Airflow: http://localhost:8080

PostgreSQL: localhost:5432

Airflow standalone prints generated admin credentials in the container logs on first startup.

## Local Pipeline Commands

After the PostgreSQL container is healthy, you can run individual steps:

```bash
python pipelines/ingestion.py
python quality/checks.py
dbt run --project-dir dbt --profiles-dir dbt
dbt test --project-dir dbt --profiles-dir dbt
streamlit run dashboard/app.py
python ai/assistant.py
```

## Warehouse Design

Schemas:

- `raw.customers`
- `analytics.stg_customers`
- `analytics.customer_metrics`
- `analytics.revenue_metrics`

The raw schema preserves loaded source records. The analytics schema contains cleaned staging views and marts used by dashboards and AI workflows.

## Replacing Sample Data

The demo data is in `pipelines/data/customers.csv`. Replace it with a real CRM, billing, product analytics, or customer success export using the same columns:

- `customer_id`
- `customer_name`
- `email`
- `country`
- `signup_date`
- `subscription_plan`
- `monthly_revenue`
- `status`

For real APIs, replace the CSV reader in `pipelines/ingestion.py` with API client logic and keep the warehouse loading contract.

## Airbyte Configuration

Airbyte is represented as a future ingestion option in this demo. To connect real systems:

1. Deploy Airbyte Cloud or OSS.
2. Configure connectors for systems such as Salesforce, HubSpot, Stripe, Shopify, PostgreSQL, or Google Sheets.
3. Land source tables into the `raw` schema.
4. Point dbt staging models at the raw connector tables.

Use placeholders such as `YOUR_API_KEY` and replace them with production environment credentials through your secret manager.

## BigQuery Configuration

To migrate to BigQuery:

1. Install the dbt BigQuery adapter.
2. Replace PostgreSQL profile settings with:
   - Google Cloud project ID: `YOUR_GCP_PROJECT_ID`
   - Dataset ID: `YOUR_DATASET_ID`
   - Service Account JSON: `YOUR_SERVICE_ACCOUNT_JSON`
3. Update ingestion to write into the BigQuery raw dataset.
4. Change dashboard queries to use BigQuery or a semantic/API layer.

Replace these values with your production environment credentials.

## Deployment Notes

- Store secrets in a cloud secret manager, not in Git.
- Run Airflow with a production metadata database and remote logging.
- Use managed warehouses such as BigQuery, Snowflake, Redshift, or Databricks for production workloads.
- Add CI checks for Python linting, dbt compilation, dbt tests, and Docker Compose validation.
- Add monitoring for ingestion freshness, row counts, schema drift, and dashboard availability.

## Offline Blueprint

Open `docs/data_platform_blueprint.html` in a browser for an offline architecture walkthrough.


## Live Demo

Dashboard:
https://analytics-platform-8o8c2ammxsak48emxxwzyy.streamlit.app/


API:
https://analytics-api.onrender.com



## Architecture

Data Sources

↓

Airbyte

↓

Warehouse

↓

dbt

↓

Dashboard

↓

AI Assistant