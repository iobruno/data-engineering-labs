{{ config(
    schema=resolve_schema_for('core')
) }}

with fhv_timedelta as (
    select
        pickup_year                                          as year,
        pickup_month                                          as month,
        pickup_zone                                           as pickup_zone,
        dropoff_zone                                          as dropoff_zone,
        datediff(second, pickup_datetime, dropoff_datetime)   as timedelta_seconds
    from
        {{ ref('dim_fhv_trips') }}
),

fhv_zone_timedelta_p90 as (
    select
        year                                                          as year,
        month                                                         as month,
        pickup_zone                                                   as pickup_zone,
        dropoff_zone                                                  as dropoff_zone,
        count(1)                                                      as num_trips,
        percentile_cont(0.90) within group (order by timedelta_seconds) as timedelta_p90
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
    num_trips               as num_trips,
    dense_rank() over (partition by year, month, pickup_zone order by timedelta_p90 desc) as rnk
from
    fhv_zone_timedelta_p90
