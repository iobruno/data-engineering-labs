# Kafka Streams with ksqlDB

[![Kafka](https://img.shields.io/badge/Confluent_Platform-8.1-141414?style=flat&logo=apachekafka&logoColor=white&labelColor=141414)](https://docs.confluent.io/platform/current/)
[![Docker](https://img.shields.io/badge/Docker-329DEE?style=flat&logo=docker&logoColor=white&labelColor=329DEE)](https://docs.docker.com/get-docker/)

![License](https://img.shields.io/badge/license-CC--BY--SA--4.0-31393F?style=flat&logo=creativecommons&logoColor=black&labelColor=white)

This contains the SQL statements to build the KStreams and KTables for ksqlDB to allow an overview of Green and FHV Trips distribution

```text
        ===========================================
        =       _              _ ____  ____       =
        =      | | _____  __ _| |  _ \| __ )      =
        =      | |/ / __|/ _` | | | | |  _ \      =
        =      |   <\__ \ (_| | | |_| | |_) |     =
        =      |_|\_\___/\__, |_|____/|____/      =
        =                   |_|                   =
        =        The Database purpose-built       =
        =        for stream processing apps       =
        ===========================================

Copyright 2017-2022 Confluent Inc.

CLI v8.1.1, Server v8.1.1 located at http://ksqldb0:808
Server Status: RUNNING

Having trouble? Type 'help' (case-insensitive) for a rundown of how things work!

ksql>
```


## Getting Started

**0.** Make sure `ksqlDB-server` and `ksql-cli` are up. Check the instructions on [README](../README.md) for more details:
```shell
docker compose -f ../compose.yml up -d
```

**1.** Connect to ksqlDB through the ksqlDB CLI:
```shell
docker exec -it ksqlcli ksql http://ksqldb0:8088
```

You should be getting into this console:
```
ksql>
```

**2.** Config ksql to default fetching offsets from 'earliest':
```shell
ksql> set 'auto.offset.reset' = 'earliest';
```

**3.** Create the KStreams for `green_tripdata` and `fhv_tripdata`:
```sql
create source stream green_tripdata_stream (
    vendor_id int,
    pickup_location_id int
) with (
    kafka_topic = 'green_tripdata',
    key_format = 'kafka',
    value_format = 'json'
);

create source stream fhv_tripdata_stream (
    dispatching_base_number varchar,
    pickup_location_id int
) with (
    kafka_topic  = 'fhv_tripdata',
    key_format   = 'kafka',
    value_format = 'json'
);
```

**4.** Create KTables to count the number of trips per location
```sql
create or replace table green_tripdata_stats with (
    kafka_topic='green_tripdata_stats',
    key_format='kafka',
    value_format='json',
    partitions=2
) as 
select
    pickup_location_id,
    count(*) as num_trips
from 
    green_tripdata_stream
group by
    pickup_location_id
emit changes;
```

```sql
create or replace table fhv_tripdata_stats with (
    kafka_topic='fhv_pickup_stats',
    key_format='kafka',
    value_format='json',
    partitions=2
) as
    select
        pickup_location_id,
        count(*) as num_trips
    from
        fhv_tripdata_stream
    group by
        pickup_location_id
    emit changes;
```

**5.** Create the KTable to joining the `green` and `fhv` tripdata:
```sql
create or replace table overall_pickup_stats with (
    kafka_topic='overall_pickup_stats',
    key_format='kafka',
    value_format='json',
    partitions=2
) as
select
    rowkey as id,
    g.pickup_location_id as green_location_id,
    f.pickup_location_id as fhv_location_id,
    coalesce(g.num_trips, CAST(0 as bigint)) as green_records,
    coalesce(f.num_trips, CAST(0 as bigint)) as fhv_records,
    coalesce(g.num_trips, CAST(0 as bigint)) + coalesce(f.num_trips, CAST(0 as bigint)) as total_records,
    1 as dummy_col -- workaround for overall_pickup_agg
    from
        green_tripdata_stats g
    full outer join
        fhv_tripdata_stats f on g.pickup_location_id = f.pickup_location_id
;
```

**6.** Create the KTable to generate the statistics on Trips distribution:
```sql
-- KTable for Statistics on Aggregation
create or replace table overall_pickup_agg with (
    kafka_topic='overall_pickup_agg',
    key_format='kafka',
    value_format='json',
    partitions=2
) as
    select
        sum(green_records) as total_green_records,
        sum(fhv_records)   as total_fhv_records,
        sum(total_records) as overall_records,
        dummy_col
    from
        overall_pickup_stats
    group by
        dummy_col
;
```

**7.** Query the statistics on Trips Distribution with:
```sql
-- Bind to the console to all updates on Query:
ksql> select * from overall_pickup_agg emit changes;

+----------------------+----------------------+----------------------+----------------------+
|DUMMY_COL             |TOTAL_GREEN_RECORDS   |TOTAL_FHV_RECORDS     |OVERALL_RECORDS       |
+----------------------+----------------------+----------------------+----------------------+
|1                     |630918                |21039983              |21670901              |
|1                     |630918                |21058899              |21689817              |
|1                     |630918                |21077704              |21708622              |
|1                     |630918                |21096012              |21726930              |
|1                     |630918                |21115601              |21746519              |
|1                     |630918                |21134044              |21764962              |
|1                     |630918                |21152782              |21783700              |
|1                     |630918                |21170356              |21801274              |
|1                     |630918                |21189974              |21820892              |
|1                     |630918                |21209372              |21840290              |
|1                     |630918                |21226677              |21857595              |
|1                     |630918                |21245814              |21876732              |
|1                     |630918                |21264974              |21895892              |
|1                     |630918                |21284161              |21915079              |
|1                     |630918                |21302856              |21933774              |
|1                     |630918                |21319461              |21950379              |
|1                     |630918                |21323952              |21954870              |
```