# Data visualization with Superset and Metabase

[![Metabase](https://img.shields.io/badge/Metabase-509EE3?style=flat&logo=metabase&logoColor=white&labelColor=65A9E7)](https://github.com/metabase/metabase)
[![BigQuery](https://img.shields.io/badge/BigQuery-3772FF?style=flat&logo=googlebigquery&logoColor=white&labelColor=3772FF)](https://console.cloud.google.com/bigquery)
[![Redshift](https://img.shields.io/badge/Redshift_Serverless-2766A7?style=flat&logo=Amazon%20RedShift&logoColor=white&labelColor=2766A7)](https://aws.amazon.com/pt/redshift/redshift-serverless/)
[![ClickHouse](https://img.shields.io/badge/ClickHouse-151515?style=flat&logo=clickhouse&logoColor=FBFD73&labelColor=151515)](https://clickhouse.com/docs/en/install)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?style=flat&logo=postgresql&logoColor=white&labelColor=336791)](https://hub.docker.com/_/postgres)

![License](https://img.shields.io/badge/license-CC--BY--SA--4.0-31393F?style=flat&logo=creativecommons&logoColor=black&labelColor=white)


## Getting Started

**1.** Spin up Metabase infrastructure with:

```shell
docker compose -f compose.metabase.yaml up -d
```

**2.** Additional database drivers:

Metabase supports a wide-variety of data sources out-of-the-box (BigQuery, Snowflake, ClickHouse, Starbust/Trino, Redshift, Spark SQL, Druid, PostgreSQL, MySQL, among others). The complete list of supported data sources can be found [here](https://www.metabase.com/data_sources/)

For Partners' and Community Data Sources, (such as ClickHouse, prior to v54.1), the additional JDBC drivers  must be downloaded into the `plugins` folder (default: `/app/plugins`)


**3.** After the `metabase-app` container is in a healthy state, you can acccess Metabase at:
```shell
open http://localhost:3000/
```


## TODO's:
- [x] Bootstrap Metabase infrastructure in Docker
- [ ] Build data viz for NYC Taxi Dataset on Metabase

