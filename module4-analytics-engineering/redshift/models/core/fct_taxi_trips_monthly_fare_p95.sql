{{ config(
    schema=resolve_schema_for('core')
) }}

with fare_percentile as (
    select
        service_type                as service_type,
        pickup_year                 as year,
        pickup_month                as month,
        fare_amount                 as fare_amount,
        percentile_disc(fare_amount, 0.97) over (partition by service_type, pickup_year, pickup_month) as p97,
        percentile_disc(fare_amount, 0.95) over (partition by service_type, pickup_year, pickup_month) as p95,
        percentile_disc(fare_amount, 0.90) over (partition by service_type, pickup_year, pickup_month) as p90
    from
        {{ ref('dim_taxi_trips') }}
    where
        fare_amount > 0
        and trip_distance > 0
        and lower(payment_type_description) in ('cash', 'credit card')
)

select
    service_type                    as service_type,
    year                            as year,
    month                           as month,
    count(1)                        as num_trips,
    round(any_value(p97), 4)        as p97_fare,
    round(any_value(p95), 4)        as p95_fare,
    round(any_value(p90), 4)        as p90_fare
from
    fare_percentile
group by
    service_type,
    year,
    month
