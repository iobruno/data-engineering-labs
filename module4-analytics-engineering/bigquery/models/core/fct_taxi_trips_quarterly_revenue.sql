{{ config(
    schema=resolve_schema_for('core')
) }}

with quarterly_trips as (
    select
        service_type                as service_type,
        pickup_year                 as year,
        pickup_quarter              as quarter,
        count(1)                    as num_trips,
        sum(total_amount)           as revenue
    from
        {{ ref('dim_taxi_trips') }}
    group by
        service_type,
        year,
        quarter
),

quarterly_trips_with_prev as (
    select
        service_type                as service_type,
        year                        as year,
        quarter                     as quarter,
        num_trips                   as num_trips,
        round(revenue, 2)           as revenue,
        lag(revenue) over (partition by service_type, quarter order by year) as prev_year_revenue
    from
        quarterly_trips
)

select
    service_type                    as service_type,
    year                            as year,
    quarter                         as quarter,
    num_trips                       as num_trips,
    revenue                         as revenue,
    round(safe_divide(revenue - prev_year_revenue, prev_year_revenue) * 100, 2) as growth
from
    quarterly_trips_with_prev
order by
    service_type,
    year desc,
    quarter desc
