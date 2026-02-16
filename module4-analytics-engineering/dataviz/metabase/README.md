# Data visualization with Metabase

[![Metabase](https://img.shields.io/badge/Metabase-509EE3?style=flat&logo=metabase&logoColor=white&labelColor=509EE3)](https://github.com/metabase/metabase)
[![BigQuery](https://img.shields.io/badge/BigQuery-262A38?style=flat&logo=googlebigquery&logoColor=white&labelColor=3772FF)](https://console.cloud.google.com/bigquery)
[![Snowflake](https://img.shields.io/badge/Snowflake-262A38?style=flat&logo=snowflake&logoColor=white&labelColor=249EDC)](https://www.snowflake.com/en/product/platform/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-262A38?style=flat&logo=postgresql&logoColor=white&labelColor=336791)](https://hub.docker.com/_/postgres)
[![ClickHouse](https://img.shields.io/badge/ClickHouse-262A38?style=flat&logo=clickhouse&logoColor=FFFFFF&labelColor=262A38)](https://clickhouse.com/docs/en/install)
[![DuckDB](https://img.shields.io/badge/DuckDB-262A38?style=flat&logo=duckdb&logoColor=FEF000&labelColor=262A38)](https://duckdb.org/docs/)

![License](https://img.shields.io/badge/license-CC--BY--SA--4.0-31393F?style=flat&logo=creativecommons&logoColor=black&labelColor=white)


## Getting Started

**1.** Start off by spinning Metabase up:

```shell
docker compose up -d
```

**2.** Metabase Initial Setup

After the `metabase` container is in a healthy state, the `metabase-setup` sidecar automatically creates the admin user (skipping the UI wizard).  You can access Metabase at:

```shell
open http://localhost:3000/
```
```txt
Email: admin@metabase.local
Password: admin
```


## Metabase additional drivers

Metabase ships with a wide variety [**Official Connectors**](https://www.metabase.com/data_sources/) out-of-the box, including BigQuery, Snowflake, ClickHouse, Starburst/Trino, etc.

For  **Community Connectors**, such as [**DuckDB**](https://github.com/motherduckdb/metabase_duckdb_driver), the JDBC driver must first be downloaded into the `plugins/`, prior to Metabase initialization  (default: `/app/plugins`), which is exactly what `metabase-init` does


## TODO's
- [x] Bootstrap Metabase infrastructure in Docker
- [x] Build data viz for NYC Taxi Dataset on Metabase
