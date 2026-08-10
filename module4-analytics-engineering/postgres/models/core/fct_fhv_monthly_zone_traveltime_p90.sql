{{ config(
    schema=resolve_schema_for('core')
) }}

with fhv_timedelta as (
    select
        pickup_year         as year,
        pickup_month        as month,
        pickup_zone         as pickup_zone,
        dropoff_zone        as dropoff_zone,
        extract(epoch from (dropoff_datetime - pickup_datetime)) as timedelta
    from
        {{ ref('dim_fhv_trips') }}
),

fhv_percentile as (
    select
        year                as year,
        month               as month,
        pickup_zone         as pickup_zone,
        dropoff_zone        as dropoff_zone,
        count(1)            as num_trips,
        percentile_cont(0.90) within group (order by timedelta) as timedelta_p90
    from
        fhv_timedelta
    group by
        year,
        month,
        pickup_zone,
        dropoff_zone
),

fhv_rnk_timedelta as (
    select
        year                as year,
        month               as month,
        pickup_zone         as pickup_zone,
        dropoff_zone        as dropoff_zone,
        num_trips           as num_trips,
        timedelta_p90       as timedelta_p90,
        dense_rank() over (partition by year, month, pickup_zone order by timedelta_p90 desc) as rnk
    from
        fhv_percentile
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
