select
    count(*) as total_customers,
    count(*) filter (where status = 'active') as active_customers,
    count(*) filter (where status = 'churned') as churned_customers,
    round(
        count(*) filter (where status = 'churned')::numeric / nullif(count(*), 0),
        4
    ) as churn_rate
from {{ ref('stg_customers') }}
