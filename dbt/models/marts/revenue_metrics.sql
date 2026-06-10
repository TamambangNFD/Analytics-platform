select
    date_trunc('month', signup_date)::date as revenue_month,
    sum(monthly_revenue) as total_revenue,
    avg(monthly_revenue) as average_revenue,
    count(*) as customer_count
from {{ ref('stg_customers') }}
group by 1
