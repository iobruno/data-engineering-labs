{{ config(
    schema=resolve_schema_for('staging')
) }}

with yellow_taxi_trips as (
    select
        row_number() over(partition by vendorid, tpep_pickup_datetime) as row_num,
        yt.*
    from
        {{ source('raw_nyc_tlc_record_data', 'yellow_trip_data') }} yt
    where
        VendorID is not null        
)

select
    -- identifiers
    {{ dbt_utils.generate_surrogate_key([
        'VendorID', 
        'tpep_pickup_datetime'
    ]) }}                                 as trip_id,
    VendorID                              as vendor_id,
    RatecodeID                            as ratecode_id,
    PULocationID                          as pickup_location_id,
    DOLocationID                          as dropoff_location_id,
    -- pickup and dropoff timestamps
    tpep_pickup_datetime                  as pickup_datetime,
    tpep_dropoff_datetime                 as dropoff_datetime,
    -- trip info
    store_and_fwd_flag                    as store_and_fwd_flag,
    passenger_count                       as passenger_count,
    trip_distance                         as trip_distance,
    1                                     as trip_type, -- yellow cabs are always street-hail
    -- payment info
    fare_amount                           as fare_amount,
    extra                                 as extra,
    mta_tax                               as mta_tax,
    tip_amount                            as tip_amount,
    tolls_amount                          as tolls_amount,
    0                                     as ehail_fee, -- it does not apply for yellow cabs
    improvement_surcharge                 as improvement_surcharge,
    congestion_surcharge                  as congestion_surcharge,
    total_amount                          as total_amount,
    payment_type                          as payment_type,
    {{ payment_desc_of('payment_type') }} as payment_type_desc
from 
    yellow_taxi_trips
where
    row_num = 1

-- Run as:
--  dbt build --select stg_green_tripdata --vars 'is_test_run: true'
--  dbt run --select stg_green_tripdata --vars 'is_test_run: false'
{% if var('is_test_run', default=false) %}
limit 100
{% endif %}
