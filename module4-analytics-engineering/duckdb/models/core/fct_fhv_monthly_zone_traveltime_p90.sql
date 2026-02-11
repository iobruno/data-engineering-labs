{{ config(
    schema=resolve_schema_for('core')
) }}

with fhv_timedelta as (
    select
        pickup_year         as year,
        pickup_month        as month,
        pickup_zone         as pickup_zone,
        dropoff_zone        as dropoff_zone,
        quantile_cont(datediff('second', pickup_datetime, dropoff_datetime), 0.90)
            over (partition by pickup_year, pickup_month, pickup_zone, dropoff_zone) as timedelta_p90
    from
        {{ ref('dim_fhv_trips') }}
),

fhv_rnk_timedelta as (
    select
        year                as year,
        month               as month,
        pickup_zone         as pickup_zone,
        dropoff_zone        as dropoff_zone,
        count(1)            as num_trips,
        max(timedelta_p90)  as timedelta_p90,
        dense_rank() over (partition by year, month, pickup_zone order by max(timedelta_p90) desc) as rnk
    from
        fhv_timedelta
    group by
        year,
        month,
        pickup_zone,
        dropoff_zone
)

select
    year                    as year,
    month                   as month,
    pickup_zone             as pickup_zone,
    dropoff_zone            as dropoff_zone,
    timedelta_p90           as timedelta_p90,
    rnk                     as rnk,
    num_trips               as num_trips
from
    fhv_rnk_timedelta
