with source as (
    select
        customer_id,
        trim(customer_name) as customer_name,
        lower(trim(email)) as email,
        trim(country) as country,
        cast(signup_date as date) as signup_date,
        trim(subscription_plan) as subscription_plan,
        cast(monthly_revenue as numeric(12, 2)) as monthly_revenue,
        lower(trim(status)) as status
    from raw.customers
)

select *
from source
