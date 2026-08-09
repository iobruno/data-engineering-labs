# dbt and DuckLake for Analytics

![Python](https://img.shields.io/badge/Python-3.14_|_3.13_|_3.12-4B8BBE.svg?style=flat&logo=python&logoColor=FFD43B&labelColor=306998)
[![dbt][dbt-shield]](https://docs.getdbt.com/reference/warehouse-setups/bigquery-setup)
[![uv](https://img.shields.io/badge/astral/uv-261230?style=flat&logo=uv&logoColor=DE5FE9&labelColor=261230)](https://docs.astral.sh/uv/getting-started/installation/)
[![DuckLake](https://img.shields.io/badge/DuckLake-1A1A1A?style=flat&logo=duckdb&logoColor=2FAFFF&labelColor=1A1A1A)](https://ducklake.select/)
[![Docker](https://img.shields.io/badge/Docker-329DEE?style=flat&logo=docker&logoColor=white&labelColor=329DEE)](https://docs.docker.com/get-docker/)

![License](https://img.shields.io/badge/license-CC--BY--SA--4.0-31393F?style=flat&logo=creativecommons&logoColor=black&labelColor=white)

Analytics engineering project using [dbt-duckdb](https://docs.getdbt.com/docs/core/connect-data-platform/duckdb-setup) to model [NYC TLC Trip Record](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page) Parquet data (Yellow Taxi, Green Taxi, and For-Hire Vehicle) into a Kimball dimensional warehouse. [Staging models](./models/staging/) feed the following dimension and fact tables:

- `dim_zone_lookup` — taxi zone dimension (borough, zone, service zone)
- `fct_taxi_trips` / `fct_fhv_trips` — trip-grain facts for Yellow/Green Taxi and FHV, denormalized with pickup/dropoff borough & zone
- `fct_taxi_monthly_zone_revenue` — monthly fare/tip/toll/surcharge revenue by pickup zone (Yellow/Green Taxi)
- `fct_taxi_trips_quarterly_revenue` — quarterly revenue with year-over-year growth (Yellow/Green Taxi)
- `fct_taxi_trips_monthly_fare_p95` — monthly p90/p95/p97 fare percentiles (Yellow/Green Taxi)
- `fct_fhv_monthly_zone_traveltime_p90` — monthly p90 travel time by pickup/dropoff zone (FHV)

Source data is Parquet-only, queried in place via `dbt-duckdb` straight from GCS, S3, or local filesystem — no raw database or ingestion step in front of it.

The warehouse itself is a [DuckLake](https://ducklake.select/) catalog served over DuckDB's [Quack](https://duckdb.org/docs/current/quack/overview) client/server protocol (see `compose.yaml`), rather than a single `.duckdb` file — so the warehouse can be queried (DBeaver, the `duckdb` CLI, another `dbt` run) while a build is in flight, and by more than one writer at a time.

> **Note:** `dim_*`/`fct_*` are materialized tables and can be queried from any client (DataGrip, DBeaver, the DuckDB UI). The `stg_*` models are **views** over the source Parquet on GCS/S3, so querying them re-reads the source in the caller's own session — which only dbt has credentials for (`filesystems:` in `profiles.tmpl.yml`). External SQL clients will get `403 Forbidden` on `stg_*`; query the materialized `dim_*`/`fct_*` models instead, or run the equivalent SQL through dbt.


## Getting Started

**1.** Install dependencies from pyproject.toml and activate the created virtualenv:
```shell
uv sync && source .venv/bin/activate
```

**2.** (Optional) Install pre-commit:
```shell
brew install pre-commit

# From root folder where `.pre-commit-config.yaml` is located, run:
pre-commit install
```

**3.** Start the DuckDB catalog server, the warehouse itself:
```shell
docker compose up -d duckdb-server
```
This runs the official `duckdb/duckdb` image (see `compose.yaml`), booted with `quack/init.sql`, which loads the Quack extension and calls `quack_serve()` so the DuckDB process behind it can be attached to as a DuckLake catalog by any number of clients — dbt included — instead of being opened as a single-writer local file.

**4.** Setup dbt profiles.yaml accordingly (use the `profiles.tmpl.yml` as template)

4.1. By default, the profiles_dir is the user '$HOME/.dbt/'
```shell
mkdir -p ~/.dbt/
cat profiles.tmpl.yml >> ~/.dbt/profiles.yml
```

4.2. Point dbt at the `duckdb-server` container and choose where DuckLake writes its Parquet data. The token must match `QUACK_TOKEN` on the server (`compose.yaml` defaults it to `quack`); host/port default to `localhost:9494`, matching the compose port mapping:
```shell
export QUACK_TOKEN=quack
export DBT_DUCKLAKE_QUACK_HOST=localhost
export DBT_DUCKLAKE_QUACK_PORT=9494
export DBT_DUCKLAKE_DATA_PATH=~/.duckdb/warehouse/
```
`DBT_DUCKLAKE_DATA_PATH` also accepts `gs://` / `s3://` to make this a genuine lakehouse — the `duckdb-server` container only ever holds catalog metadata, never the Parquet data itself, so it needs no object-store credentials of its own.

> **Note:** `DATA_PATH` is recorded in the catalog the first time you `ATTACH` — changing the env var afterwards does not move existing data (DuckLake's `OVERRIDE_DATA_PATH` does not yet work against a Quack catalog). To point at a different location, attach a fresh catalog (i.e. restart `duckdb-server` against an empty volume).

4.3. Set the auth methods (when applicable) and the ENV variables for the source data DuckDB reads from:

**Google Cloud Storage (gcsfs)** - when attempting to read data from `gcs`, first you must authenticate with:
```shell
gcloud auth login
```
```shell
export DBT_DUCKDB_SOURCE_PARQUET_BASE_PATH="gs://iobruno-lakehouse-raw/nyc_tlc_dataset/"
```

**AWS S3 (s3fs)** - when attempting to read data from `s3`, first you must set these AWS ENV VARS:
```shell
export AWS_ACCESS_KEY=
export AWS_SECRET_ACCESS_KEY=
```
```shell
export DBT_DUCKDB_SOURCE_PARQUET_BASE_PATH="s3://iobruno-lakehouse-raw/nyc_tlc_dataset/"
```

**Local FS** - no additional config required
```shell
export DBT_DUCKDB_SOURCE_PARQUET_BASE_PATH="/path-to/nyc_tlc_dataset/"
```

4.4. (Optional) you can also set the DuckDB schemas where the dbt staging & core models should land on:
```shell
# DuckDB schema for the `dim_` and `fct_ models` - defaults to 'main' if not set
export DBT_DUCKDB_TARGET_SCHEMA=analytics

# DuckDB for the stg_ models - defaults to 'main' if not set
export DBT_DUCKDB_STAGING_SCHEMA=stg_analytics
```

**5.** Install dbt dependencies and trigger the pipeline

5.1. Run `dbt deps` to install  dbt plugins
```shell
dbt deps
```

5.2. Run dbt build to trigger the dbt models to run
```shell
dbt build

# Alternatively you can run only a subset of the models with:

## +models/staging: Runs the dependencies/preceding models first that lead 
## to 'models/staging', and then the target models
dbt build --select +models/staging

## models/staging+: Runs the target models first, and then all models that depend on it
dbt build --select models/staging+
```

**6.** Generate the Docs and the Data Lineage graph with:
```shell
dbt docs generate
dbt docs serve
```

Access the generated docs at:
```shell
open http://localhost:8080
```


## Containerization
The warehouse (`duckdb-server`) runs containerized via `compose.yaml`, as described in step 3 above. Containerizing the `dbt` CLI run itself is T.B.D.


## Connecting External Clients
SQL clients using the DuckDB JDBC driver (DataGrip, DBeaver, ...) can attach to the warehouse via `quack/client_init.sql` as the session init script, mirroring what `profiles.tmpl.yml` does for dbt:

```
jdbc:duckdb:;session_init_sql_file=/path/to/client_init.sql;jdbc_stream_results=true;jdbc_pin_db=true;
```

As noted above, this only gets you `dim_*`/`fct_*` tables — `stg_*` views still require dbt's GCS credentials.

Alternatively, `docker compose up -d duckdb-ui` starts a container that runs the same bootstrap plus DuckDB's web UI, browsable at `http://localhost:4213`.


## TODO's:
- [x] PEP-517: Packaging and dependency management with `uv`
- [x] Bootstrap dbt with DuckDB Adapter ([dbt-duckdb](https://github.com/duckdb/dbt-duckdb))
- [x] Configure dbt-duckdb with `fsspec` and read from [gcsfs](https://gcsfs.readthedocs.io/en/latest/api.html?highlight=GCSFileSystem#gcsfs.core.GCSFileSystem)
- [x] Configure dbt-duckdb with `fsspec` and read from [s3fs](https://s3fs.readthedocs.io/en/latest/api.html#s3fs.core.S3FileSystem)
- [x] Run the warehouse as a client/server daemon with [DuckLake](https://ducklake.select/) on a [Quack](https://duckdb.org/docs/current/quack/overview)-served DuckDB catalog
- [x] Implement Data Observability with [elementary-data](https://github.com/elementary-data/elementary)
- [ ] Implement Data Quality metrics it with [dbt-expectations](https://github.com/metaplane/dbt-expectations/)


<!-- Reference-style image def, kept out of the badge row above -->
[dbt-shield]: https://img.shields.io/badge/dbt--core-1.12-262A38?style=flat&labelColor=262A38&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIGZpbGw9IiNmZjY5NGIiIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZD0iTTE3LjkgOS4zOGE4IDggMCAwIDAtMy4wNC0zLjEybDEuNzcuODNhMTAgMTAgMCAwIDEgMy43NCAzbDMuMjMtNS45M2EyLjkgMi45IDAgMCAwLS4wNi0yLjk2IDIuNzMgMi43MyAwIDAgMC0zLjU2LS44N0wxNC4xIDMuNTRhNC40IDQuNCAwIDAgMS00LjE4IDBMNC4xOC40MWEyLjkgMi45IDAgMCAwLTIuOTYuMDYgMi43MyAyLjczIDAgMCAwLS44OCAzLjU3TDMuNTYgOS45YTQuNCA0LjQgMCAwIDEgMCA0LjE4TC40MiAxOS44M2EyLjkgMi45IDAgMCAwIC4wOSAzIDIuNzMgMi43MyAwIDAgMCAzLjU0Ljg0bDYuMDYtMy4zYTEwIDEwIDAgMCAxLTMtMy43NmwtLjg0LTEuNzdhOCA4IDAgMCAwIDMuMTIgMy4wNWwxMC41OCA1Ljc4YTIuNzMgMi43MyAwIDAgMCAzLjU1LS44NCAyLjkgMi45IDAgMCAwIC4wOC0zem0zLjM4LTcuNzRhMS4wOSAxLjA5IDAgMSAxIDAgMi4xOCAxLjA5IDEuMDkgMCAwIDEgMC0yLjE4TTIuNzQgMy44MmExLjA5IDEuMDkgMCAxIDEgMC0yLjE4IDEuMDkgMS4wOSAwIDAgMSAwIDIuMThtMCAxOC41NGExLjA5IDEuMDkgMCAxIDEgMC0yLjE4IDEuMDkgMS4wOSAwIDAgMSAwIDIuMThNMTMuMSAxMC45YTIuMTcgMi4xNyAwIDAgMC0yLjE4IDIuMTcgMi4yIDIuMiAwIDAgMCAuNyAxLjYgMi43MiAyLjcyIDAgMSAxIC43Ny01LjM4IDIuNyAyLjcgMCAwIDEgMi4zIDIuMzIgMi4yIDIuMiAwIDAgMC0xLjU5LS43MW04LjE4IDExLjQ1YTEuMDkgMS4wOSAwIDEgMSAwLTIuMTggMS4wOSAxLjA5IDAgMCAxIDAgMi4xOCIvPjwvc3ZnPgo=
