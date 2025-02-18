{{ config(
    schema=resolve_schema_for('core')
) }}

with fhv_timedelta as (
  select 
    pickup_year         as year, 
    pickup_month        as month,
    pickup_location_id,
    dropoff_location_id,
    percentile_cont(timestamp_diff(dropoff_datetime, pickup_datetime, SECOND), 0.90)
      over (partition by pickup_year, pickup_month, pickup_location_id, dropoff_location_id) as timedelta_p90
  from
    {{ ref('dim_fhv_trips') }}
),

fhv_rnk_timedelta as (
  select
      year, 
      month,
      pickup_location_id,
      dropoff_location_id,
      count(1) as num_trips,
      max(timedelta_p90) as timedelta_p90,
      dense_rank() over (partition by year, month, pickup_location_id order by max(timedelta_p90) desc) as rnk
  from 
    fhv_timedelta
  group by
    year,
    month,
    pickup_location_id,
    dropoff_location_id
)

select 
  year          as year,
  month         as month,
  pz.zone       as pickup_zone,
  dz.zone       as dropoff_zone,
  timedelta_p90 as timedelta_p90,
  rnk           as rnk,
  num_trips     as num_trips

from 
  fhv_rnk_timedelta fhv
inner join 
    {{ ref('dim_zone_lookup' )}} pz on fhv.pickup_location_id = pz.location_id
inner join 
    {{ ref('dim_zone_lookup' )}} dz on fhv.dropoff_location_id = dz.location_id
order by
  year, month, pickup_location_id
