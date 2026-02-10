{{ config(
    schema=resolve_schema_for('core')
) }}

with lookup_zones as (
    select location_id, borough, zone, service_zone
    from {{ ref('dim_zone_lookup') }}
    where borough != 'Unknown'
)

select
    ft.trip_id,
    ft.dispatching_base_num,
    ft.affiliated_base_num,
    ft.shared_ride_flag,

    ft.pickup_location_id,
    pu.borough                                  as pickup_borough,
    pu.zone                                     as pickup_zone,
    pu.service_zone                             as pickup_service_zone,

    ft.dropoff_location_id,
    do.borough                                  as dropoff_borough,
    do.zone                                     as dropoff_zone,
    do.service_zone                             as dropoff_service_zone,

    ft.pickup_datetime,
    extract(year from ft.pickup_datetime)       as pickup_year,
    extract(quarter from ft.pickup_datetime)    as pickup_quarter,
    extract(month from ft.pickup_datetime)      as pickup_month,

    ft.dropoff_datetime,
    extract(year from ft.dropoff_datetime)      as dropoff_year,
    extract(quarter from ft.dropoff_datetime)   as dropoff_quarter,
    extract(month from ft.dropoff_datetime)     as dropoff_month
from
    {{ ref('stg_fhv_tripdata') }} ft
inner join
    lookup_zones pu on ft.pickup_location_id = pu.location_id
inner join
    lookup_zones do on ft.dropoff_location_id = do.location_id
