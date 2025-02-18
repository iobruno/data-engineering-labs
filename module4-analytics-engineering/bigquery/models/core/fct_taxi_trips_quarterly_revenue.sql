{{ config(
    schema=resolve_schema_for('core')
) }}

with quarterly_trips as (
    select
        service_type        as service_type,
        pickup_year         as year,
        pickup_quarter      as quarter,
        count(1)            as num_trips,
        sum(total_amount)   as revenue
    from 
        {{ ref('dim_taxi_trips') }}
    group by 
        service_type, 
        year, 
        quarter
)

select 
    cur.service_type                                            as service_type,
    cur.year                                                    as year,
    cur.quarter                                                 as quarter,
    format("%'d", cur.num_trips)                                as num_trips,
    format("%'.2f", round(cur.revenue, 2))                      as revenue,    
    round(((cur.revenue - prev.revenue)/prev.revenue)*100, 10)  as growth
from
    quarterly_trips cur
left join
    quarterly_trips prev on (
        cur.service_type = prev.service_type
        and cur.quarter = prev.quarter
        and (cur.year - 1) = prev.year
    )
order by
    cur.service_type,
    cur.year desc,
    cur.quarter desc
