# Data Flow

## 1. Source Data

The demo uses `pipelines/data/customers.csv`. This file represents a business export from a CRM, billing platform, or customer data API.

## 2. Ingestion

`pipelines/ingestion.py` reads the CSV, validates expected columns, cleans fields, converts types, and loads the result into `raw.customers`.

## 3. Quality

`quality/checks.py` verifies:

- `customer_id` is present and unique.
- required descriptive fields are populated.
- `monthly_revenue` is numeric and non-negative.
- the schema matches the expected contract.

## 4. Transformation

dbt creates:

- `analytics.stg_customers`
- `analytics.customer_metrics`
- `analytics.revenue_metrics`

## 5. Analytics

The dashboard reads warehouse tables when available. If the database is offline, it falls back to the demo CSV so stakeholders can still view the application.

## 6. AI Workflow

`ai/assistant.py` answers common metric questions with deterministic logic. In production, replace this with LangChain, an LLM, guardrails, and a SQL agent connected to curated analytics models.
