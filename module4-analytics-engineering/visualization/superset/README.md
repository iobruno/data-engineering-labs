# Data visualization with Superset and Metabase

[![Superset](https://img.shields.io/badge/Superset-0A2933?style=flat&logo=apache&logoColor=F8FDFF&labelColor=0A2933)](https://github.com/apache/superset)
[![BigQuery](https://img.shields.io/badge/BigQuery-3772FF?style=flat&logo=googlebigquery&logoColor=white&labelColor=3772FF)](https://console.cloud.google.com/bigquery)
[![Redshift](https://img.shields.io/badge/Redshift_Serverless-2766A7?style=flat&logo=Amazon%20RedShift&logoColor=white&labelColor=2766A7)](https://aws.amazon.com/pt/redshift/redshift-serverless/)
[![ClickHouse](https://img.shields.io/badge/ClickHouse-151515?style=flat&logo=clickhouse&logoColor=FBFD73&labelColor=151515)](https://clickhouse.com/docs/en/install)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?style=flat&logo=postgresql&logoColor=white&labelColor=336791)](https://hub.docker.com/_/postgres)

![License](https://img.shields.io/badge/license-CC--BY--SA--4.0-31393F?style=flat&logo=creativecommons&logoColor=black&labelColor=white)


## Getting Started

**0.** (Optional) Pre-loaded examples (demo charts/dashboards):

Superset can be bootstrapped withexample charts and dashboards. In order to enable that, set:
```shell
export SUPERSET_LOAD_EXAMPLES=yes
```

Make sure to: `unset SUPERSET_LOAD_EXAMPLES` or `export SUPERSET_LOAD_EXAMPLES=no`  after the **first run** of `superset-init` is completed successfully, as `load_examples` alone can take a few minutes.

**1.** Spin up Apache Superset infrastructure with:
```shell
docker compose -f compose.yaml up -d
```

**2.** Additional database drivers:

Superset supports PostgreSQL, MySQL and out-of-the-box. To enable additional data sources, include the respective `SQLAlchemy` driver as a dependency in [requirements-local.txt](./conf/requirements-local.txt). 

A complete list of supported data sources can be found [here](https://superset.apache.org/docs/databases/installing-database-drivers/).

```text
clickhouse-connect==0.8.15
sqlalchemy-bigquery==1.12.1
sqlalchemy-redshift==0.8.14
```

**3.** After the `superset-app` container is in a healthy state, you can acccess Superset at:
```shell
open http://localhost:8088/
```
**Username**: admin  
**Password**: admin


## TODO's:
- [x] Bootstrap Apache Superset infrastructure in Docker
- [ ] Build data viz for NYC Taxi Dataset on Superset

