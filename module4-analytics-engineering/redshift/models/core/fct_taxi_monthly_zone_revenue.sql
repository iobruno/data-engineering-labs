{{ config(
    schema=resolve_schema_for('core')
) }}

select
    -- Revenue Grouping
    pickup_zone                                  as zone,
    service_type                                 as service_type,
    {{ date_trunc("month", "pickup_datetime") }} as revenue_month,
    -- Revenue Calculations
    round(sum(fare_amount), 2)                   as fare,
    round(sum(extra), 2)                         as extra,
    round(sum(mta_tax), 2)                       as mta_tax,
    round(sum(tip_amount), 2)                    as tip_amount,
    round(sum(tolls_amount), 2)                  as tolls_amount,
    round(sum(ehail_fee), 2)                     as ehail_fee,
    round(sum(improvement_surcharge), 2)         as improvement_surcharge,
    round(sum(congestion_surcharge), 2)          as congestion_surcharge,
    round(sum(total_amount), 2)                  as total_amount
from
    {{ ref('dim_taxi_trips') }}
group by
    pickup_zone,
    service_type,
    {{ date_trunc("month", "pickup_datetime") }}
