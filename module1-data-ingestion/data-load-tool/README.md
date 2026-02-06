# dltHub: data load tool

![Python](https://img.shields.io/badge/Python-3.13_|_3.12-4B8BBE.svg?style=flat&logo=python&logoColor=FFD43B&labelColor=306998)
[![dltHub](https://img.shields.io/badge/dltHub-1.21-59C1D5?style=flat&logo=pandas&logoColor=59C1D5&labelColor=191937)](https://dlthub.com/docs/dlt-ecosystem/verified-sources)
[![Polars](https://img.shields.io/badge/polars-24292E?style=flat&logo=polars&logoColor=CC792B&labelColor=24292E)](https://docs.pola.rs/)
[![uv](https://img.shields.io/badge/astral/uv-261230?style=flat&logo=uv&logoColor=DE5FE9&labelColor=261230)](https://docs.astral.sh/uv/getting-started/installation/)
[![DuckDB](https://img.shields.io/badge/DuckDB-0D0D0D?style=flat&logo=duckdb&logoColor=FEF000&labelColor=0D0D0D)](https://duckdb.org/)

![License](https://img.shields.io/badge/license-CC--BY--SA--4.0-31393F?style=flat&logo=creativecommons&logoColor=black&labelColor=white)

This is meant for experimenting with [data load tool (dlt)](https://dlthub.com/) for fetching data from APIs and persiting it to a local DuckDB, Google CloudStorage, and BigQuery.


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

**3.** Run the dlt pipeline
```shell
T.B.D.
```


## TODO's:
- [x] PEP-517: Packaging and dependency management with `uv`
- [ ] Extract data from Web APIs with dlt
- [x] Code format/lint with `ruff`
