{{ config(
    schema=resolve_schema_for('core')
) }}

with taxi_trips as (
    select *, 'green' as service_type from {{ ref('stg_green_tripdata') }}
    union all
    select *, 'yellow' as service_type from {{ ref('stg_yellow_tripdata') }}
),

lookup_zones as (
    select location_id, borough, zone
    from {{ ref('dim_zone_lookup') }}
    where borough != 'Unknown'
)

select
    tt.trip_id,
    tt.vendor_id,
    tt.service_type,
    tt.ratecode_id,

    tt.pickup_location_id,
    pu.borough                                  as pickup_borough,
    pu.zone                                     as pickup_zone,
    tt.pickup_datetime,
    extract(year from tt.pickup_datetime)       as pickup_year,
    extract(quarter from tt.pickup_datetime)    as pickup_quarter,
    extract(month from tt.pickup_datetime)      as pickup_month,

    tt.dropoff_location_id,
    do.borough                                  as dropoff_borough,
    do.zone                                     as dropoff_zone,
    tt.dropoff_datetime,
    extract(year from tt.dropoff_datetime)      as dropoff_year,
    extract(quarter from tt.dropoff_datetime)   as dropoff_quarter,
    extract(month from tt.dropoff_datetime)     as dropoff_month,

    tt.store_and_fwd_flag,
    tt.passenger_count,
    tt.trip_distance,
    tt.trip_type,
    tt.fare_amount,
    tt.extra,
    tt.mta_tax,
    tt.tip_amount,
    tt.tolls_amount,
    tt.ehail_fee,
    tt.improvement_surcharge,
    tt.total_amount,
    tt.congestion_surcharge,
    tt.payment_type,
    tt.payment_type_desc                        as payment_type_description
from
    taxi_trips tt
inner join 
    lookup_zones pu on tt.pickup_location_id = pu.location_id
inner join 
    lookup_zones do on tt.dropoff_location_id = do.location_id
