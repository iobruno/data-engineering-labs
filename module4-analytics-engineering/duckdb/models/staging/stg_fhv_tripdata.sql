{{ config(
    schema=resolve_schema_for('staging')
) }}


select
    -- identifiers
    {{ dbt_utils.generate_surrogate_key([
        'dispatching_base_num',
        'pickup_datetime'
    ]) }}                  as trip_id,
    dispatching_base_num   as dispatching_base_num,
    Affiliated_base_number as affiliated_base_num,
    -- pickup and dropoff timestamps
    pickup_datetime        as pickup_datetime,
    dropOff_datetime       as dropoff_datetime,
    -- trip info
    PUlocationID           as pickup_location_id,
    DOlocationID           as dropoff_location_id,
    SR_Flag                as shared_ride_flag
from
    {{ source('raw_nyc_tlc_record_data', 'ext_fhv') }}
where
    dispatching_base_num is not null
qualify
    row_number() over(partition by dispatching_base_num, pickup_datetime) = 1

-- Run as:
--  dbt build --select stg_fhv_tripdata --vars 'is_test_run: true'
--  dbt run --select stg_fhv_tripdata --vars 'is_test_run: false'
{% if var('is_test_run', default=false) %}
limit 100
{% endif %}
