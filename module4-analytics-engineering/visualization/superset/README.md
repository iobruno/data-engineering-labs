# Data visualization with Superset

[![Superset](https://img.shields.io/badge/Superset-262A38?style=flat&logo=apachesuperset&logoColor=1EA7C9&labelColor=262A38)](https://superset.apache.org/)
[![BigQuery](https://img.shields.io/badge/BigQuery-262A38?style=flat&logo=googlebigquery&logoColor=white&labelColor=3772FF)](https://console.cloud.google.com/bigquery)
[![Snowflake](https://img.shields.io/badge/Snowflake-262A38?style=flat&logo=snowflake&logoColor=white&labelColor=249EDC)](https://www.snowflake.com/en/product/platform/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-262A38?style=flat&logo=postgresql&logoColor=white&labelColor=336791)](https://hub.docker.com/_/postgres)
[![ClickHouse](https://img.shields.io/badge/ClickHouse-262A38?style=flat&logo=clickhouse&logoColor=FFFFFF&labelColor=262A38)](https://clickhouse.com/docs/en/install)
[![DuckDB](https://img.shields.io/badge/DuckDB-262A38?style=flat&logo=duckdb&logoColor=FEF000&labelColor=262A38)](https://duckdb.org/docs/)

![License](https://img.shields.io/badge/license-CC--BY--SA--4.0-31393F?style=flat&logo=creativecommons&logoColor=black&labelColor=white)


## Getting Started

**1.** Spin up Apache Superset infrastructure with:
```shell
docker compose up -d
```

**2.** After the `superset-app` container is healthy, access Superset at [http://localhost:8088](http://localhost:8088/)

```text
Username: admin
Password: admin
```

### Pre-loaded examples

If you'd like Superset to come with example charts and dashboards, set this **before the first run**:
```shell
export SUPERSET_LOAD_EXAMPLES=yes
```

Once `superset-init` finishes, make sure to disable it so the examples aren't re-loaded on every restart:
```shell
unset SUPERSET_LOAD_EXAMPLES
```

### Additional database drivers

Superset supports PostgreSQL and MySQL out-of-the-box. To enable additional data sources, add the respective `SQLAlchemy` driver to [requirements-local.txt](./conf/requirements-local.txt). See the full list of [supported databases](https://superset.apache.org/docs/databases/)
```text
clickhouse-connect==0.8.15
sqlalchemy-bigquery==1.12.1
sqlalchemy-redshift==0.8.14
```


## TODO's
- [x] Bootstrap Apache Superset infrastructure in Docker
- [x] Build data viz for NYC Taxi Dataset on Superset
