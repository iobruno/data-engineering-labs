# Workflow orchestration with Prefect

![Python](https://img.shields.io/badge/Python-3.12-4B8BBE.svg?style=flat&logo=python&logoColor=FFD43B&labelColor=306998)
[![Prefect](https://img.shields.io/badge/Prefect-3.1-060F11?style=flat&logo=prefect&logoColor=white&labelColor=060F11)](https://www.prefect.io/opensource/)
[![Pandas](https://img.shields.io/badge/pandas-150458?style=flat&logo=pandas&logoColor=E70488&labelColor=150458)](https://pandas.pydata.org/docs/user_guide/)
[![uv](https://img.shields.io/badge/astral/uv-261230?style=flat&logo=uv&logoColor=DE5FE9&labelColor=261230)](https://docs.astral.sh/uv/getting-started/installation/)
[![Docker](https://img.shields.io/badge/Docker-329DEE?style=flat&logo=docker&logoColor=white&labelColor=329DEE)](https://docs.docker.com/get-docker/)

![License](https://img.shields.io/badge/license-CC--BY--SA--4.0-31393F?style=flat&logo=creativecommons&logoColor=black&labelColor=white)


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

**3.** Start the Prefect Server:

**Note**: The `Prefect Orion` server is now called `Prefect Server`

```shell
prefect server start
```

**4.** Setup Prefect server for the flows:
```shell
prefect config set PREFECT_API_URL=http://localhost:4200/api
```

## Prefect Flows

#### flows/web_csv_to_gcs.py:
Set the `GOOGLE_APPLICATION_CREDENTIALS` env variable:
```shell
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/gcs_credentials.json
```

Then, execute with:
```shell
python flows/web_csv_to_gcs.py
```

#### flows/sqlalchemy_ingest.py:
Set the environment variables:
```shell
export DB_USERNAME=postgres
export DB_PASSWORD=postgres
export DB_HOST=localhost
export DB_PORT=5432
export DB=nyc_taxi
```

Now, execute it with:
```shell
python flows/sqlalchemy_ingest.py
```


## TODO's:
- [x] PEP-517: Packaging and dependency management with `uv`
- [x] Deploy Prefect Server / Agent on Docker
- [x] Code format/lint with Ruff
- [ ] Run Prefect flows on Docker
