# Analytics Platform Architecture

## Overview

This repository demonstrates a production-style analytics platform that runs locally with sample data and can be adapted to real company systems.

```text
Data Sources
    |
    v
Ingestion Layer
Python pipelines / future Airbyte connectors
    |
    v
Raw Data Layer
PostgreSQL raw schema / BigQuery compatible
    |
    v
Transformation Layer
dbt staging and marts
    |
    v
Analytics Layer
analytics schema
    |
    v
Dashboard + AI Assistant
Streamlit and rule-based assistant
```

## Components

- PostgreSQL simulates the data warehouse locally.
- Python ingestion loads CSV exports into `raw.customers`.
- Data quality checks validate schema, nulls, duplicates, and revenue values.
- dbt transforms raw data into staging and analytics marts.
- Airflow orchestrates ingestion, validation, transformation, and dashboard refresh placeholders.
- Streamlit displays stakeholder-facing metrics and charts.
- The AI assistant demonstrates an AI-ready analytics interface using rule-based logic.

## BigQuery Migration

To migrate from PostgreSQL to BigQuery, replace the local database connection with:

- Google Cloud project ID: `YOUR_GCP_PROJECT_ID`
- Dataset ID: `YOUR_DATASET_ID`
- Service Account JSON: `YOUR_SERVICE_ACCOUNT_JSON`

Then update `dbt/profiles.yml` to use the dbt BigQuery adapter and configure ingestion to write to the BigQuery raw dataset.
