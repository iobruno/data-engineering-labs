{{ config(
    schema=resolve_schema_for('core')
) }}

with fhv_timedelta as (
    select
        pickup_year          as year,
        pickup_month         as month,
        pickup_zone          as pickup_zone,
        dropoff_zone         as dropoff_zone,
        timestamp_diff(dropoff_datetime, pickup_datetime, SECOND) as trip_duration_seconds
    from
        {{ ref('dim_fhv_trips') }}
    where
        dropoff_datetime > pickup_datetime
        and timestamp_diff(dropoff_datetime, pickup_datetime, SECOND) < 86400
),

fhv_rnk_timedelta as (
    select
        year                                          as year,
        month                                         as month,
        pickup_zone                                   as pickup_zone,
        dropoff_zone                                  as dropoff_zone,
        count(1)                                      as num_trips,
        percentile_cont(trip_duration_seconds, 0.90)  as timedelta_p90
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
    dense_rank() over (partition by year, month, pickup_zone order by timedelta_p90 desc) as rnk,
    num_trips               as num_trips
from
    fhv_rnk_timedelta
