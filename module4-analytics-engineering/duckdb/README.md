# dbt and DuckDB for Analytics

![Python](https://img.shields.io/badge/Python-3.13_|_3.12-4B8BBE.svg?style=flat&logo=python&logoColor=FFD43B&labelColor=306998)
[![dbt](https://img.shields.io/badge/dbt--duckdb-1.10-262A38?style=flat&labelColor=262A38&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIGZpbGw9IiNmZjY5NGIiIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZD0iTTE3LjkgOS4zOGE4IDggMCAwIDAtMy4wNC0zLjEybDEuNzcuODNhMTAgMTAgMCAwIDEgMy43NCAzbDMuMjMtNS45M2EyLjkgMi45IDAgMCAwLS4wNi0yLjk2IDIuNzMgMi43MyAwIDAgMC0zLjU2LS44N0wxNC4xIDMuNTRhNC40IDQuNCAwIDAgMS00LjE4IDBMNC4xOC40MWEyLjkgMi45IDAgMCAwLTIuOTYuMDYgMi43MyAyLjczIDAgMCAwLS44OCAzLjU3TDMuNTYgOS45YTQuNCA0LjQgMCAwIDEgMCA0LjE4TC40MiAxOS44M2EyLjkgMi45IDAgMCAwIC4wOSAzIDIuNzMgMi43MyAwIDAgMCAzLjU0Ljg0bDYuMDYtMy4zYTEwIDEwIDAgMCAxLTMtMy43NmwtLjg0LTEuNzdhOCA4IDAgMCAwIDMuMTIgMy4wNWwxMC41OCA1Ljc4YTIuNzMgMi43MyAwIDAgMCAzLjU1LS44NCAyLjkgMi45IDAgMCAwIC4wOC0zem0zLjM4LTcuNzRhMS4wOSAxLjA5IDAgMSAxIDAgMi4xOCAxLjA5IDEuMDkgMCAwIDEgMC0yLjE4TTIuNzQgMy44MmExLjA5IDEuMDkgMCAxIDEgMC0yLjE4IDEuMDkgMS4wOSAwIDAgMSAwIDIuMThtMCAxOC41NGExLjA5IDEuMDkgMCAxIDEgMC0yLjE4IDEuMDkgMS4wOSAwIDAgMSAwIDIuMThNMTMuMSAxMC45YTIuMTcgMi4xNyAwIDAgMC0yLjE4IDIuMTcgMi4yIDIuMiAwIDAgMCAuNyAxLjYgMi43MiAyLjcyIDAgMSAxIC43Ny01LjM4IDIuNyAyLjcgMCAwIDEgMi4zIDIuMzIgMi4yIDIuMiAwIDAgMC0xLjU5LS43MW04LjE4IDExLjQ1YTEuMDkgMS4wOSAwIDEgMSAwLTIuMTggMS4wOSAxLjA5IDAgMCAxIDAgMi4xOCIvPjwvc3ZnPgo=)](https://docs.getdbt.com/reference/warehouse-setups/bigquery-setup)
[![uv](https://img.shields.io/badge/astral/uv-261230?style=flat&logo=uv&logoColor=DE5FE9&labelColor=261230)](https://docs.astral.sh/uv/getting-started/installation/)
[![Docker](https://img.shields.io/badge/Docker-329DEE?style=flat&logo=docker&logoColor=white&labelColor=329DEE)](https://docs.docker.com/get-docker/)

![License](https://img.shields.io/badge/license-CC--BY--SA--4.0-31393F?style=flat&logo=creativecommons&logoColor=black&labelColor=white)

Analytics engineering project built with [`dbt`](https://docs.getdbt.com) and the [`dbt-duckdb`](https://docs.getdbt.com/docs/core/connect-data-platform/duckdb-setup) adapter that transforms [NYC TLC Trip Record](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page) Parquet data into a Kimball dimensional model — from raw ingestion through staging views to materialized dimensions and fact tables covering zone-level revenue, fare percentiles, travel time distributions, and year-over-year growth across Yellow Taxi, Green Taxi, and For-Hire Vehicle services. Supports sourcing data from GCS, S3, or local filesystem.


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

**3.** Setup dbt profiles.yaml accordingly (use the `profiles.tmpl.yml` as template)

3.1. By default, the profiles_dir is the user '$HOME/.dbt/'
```shell
mkdir -p ~/.dbt/
cat profiles.tmpl.yml >> ~/.dbt/profiles.yml
```

3.2. Set the auth methods (when appliable) and the ENV variables for DuckDB source and destination:

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

3.3. Set the env var for where DuckDB should store its internal data
```shell
export DBT_DUCKDB_TARGET_PATH=~/.duckdb/dbt.duckdb
```

3.4. (Optional) you can also set the DuckDB schemas where the dbt staging & core models should land on:
```shell
# DuckDB schema for the `dim_` and `fct_ models` - defaults to 'main' if not set
export DBT_DUCKDB_TARGET_SCHEMA=analytics=

# DuckDB for the stg_ models - defaults to 'main' if not set
export DBT_DUCKDB_STAGING_SCHEMA=stg_analytics=
```

**4.** Install dbt dependencies and trigger the pipeline

4.1. Run `dbt deps` to install  dbt plugins
```shell
dbt deps
```

4.2. Run dbt build to trigger the dbt models to run
```shell
dbt build

# Alternatively you can run only a subset of the models with:

## +models/staging: Runs the dependencies/preceding models first that lead 
## to 'models/staging', and then the target models
dbt [build|run] --select +models/staging

## models/staging+: Runs the target models first, and then all models that depend on it
dbt [build|run] --select models/staging+
```

**5.** Generate the Docs and the Data Lineage graph with:
```shell
dbt docs generate
dbt docs serve
```

Access the generated docs at:
```shell
open http://localhost:8080
```


## Containerization

**1.** Build the Docker Image with:
```shell
docker build -t dbt-duckdb:latest . --no-cache
```

**2.** Start a container with it:
```shell
docker run -d --rm \
  -e DBT_DUCKDB_SOURCE_PARQUET_BASE_PATH="gs://iobruno-lakehouse-raw/nyc_tlc_dataset/" \
  -e DBT_DUCKDB_TARGET_PATH=/duckdb/dbt.duckdb \
  -e DBT_DUCKDB_TARGET_SCHEMA=analytics \
  -v ~/.duckdb:/duckdb \
  -v PATH/TO/YOUR/gcp_credentials.json:/secrets/gcp_credentials.json \
  --name dbt-duckdb \
  dbt-duckdb
```


## TODO's:
- [x] PEP-517: Packaging and dependency management with `uv`
- [x] Bootstrap dbt with DuckDB Adapter ([dbt-duckdb](https://github.com/duckdb/dbt-duckdb))
- [x] Configure dbt-duckdb with `fsspec` and read from [gcsfs](https://gcsfs.readthedocs.io/en/latest/api.html?highlight=GCSFileSystem#gcsfs.core.GCSFileSystem)
- [x] Configure dbt-duckdb with `fsspec` and read from [s3fs](https://s3fs.readthedocs.io/en/latest/api.html#s3fs.core.S3FileSystem)
