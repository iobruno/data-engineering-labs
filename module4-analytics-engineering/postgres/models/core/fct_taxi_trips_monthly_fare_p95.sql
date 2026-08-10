{{ config(
    schema=resolve_schema_for('core')
) }}

with fare_percentile as (
    select
        service_type                as service_type,
        pickup_year                 as year,
        pickup_month                as month,
        fare_amount                 as fare_amount
    from
        {{ ref('dim_taxi_trips') }}
    where
        fare_amount > 0
        and trip_distance > 0
        and lower(payment_type_description) in ('cash', 'credit card')
)

select
    service_type                                                          as service_type,
    year                                                                   as year,
    month                                                                  as month,
    count(1)                                                               as num_trips,
    round(percentile_disc(0.97) within group (order by fare_amount), 4)   as p97_fare,
    round(percentile_disc(0.95) within group (order by fare_amount), 4)   as p95_fare,
    round(percentile_disc(0.90) within group (order by fare_amount), 4)   as p90_fare
from
    fare_percentile
group by
    service_type,
    year,
    month
