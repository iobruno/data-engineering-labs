# Workflow orchestration with Airflow 2.x

![Python](https://img.shields.io/badge/Python-3.11-4B8BBE.svg?style=flat&logo=python&logoColor=FFD43B&labelColor=306998)
[![Airflow](https://img.shields.io/badge/Airflow-2.10-007CEE?style=flat&logo=apacheairflow&logoColor=white&labelColor=14193A)](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/taskflow.html)
[![Pandas](https://img.shields.io/badge/pandas-150458?style=flat&logo=pandas&logoColor=E70488&labelColor=150458)](https://pandas.pydata.org/docs/user_guide/)
[![uv](https://img.shields.io/badge/astral/uv-261230?style=flat&logo=uv&logoColor=DE5FE9&labelColor=261230)](https://docs.astral.sh/uv/getting-started/installation/)
[![Docker](https://img.shields.io/badge/Docker-329DEE?style=flat&logo=docker&logoColor=white&labelColor=329DEE)](https://docs.docker.com/get-docker/)

![License](https://img.shields.io/badge/license-CC--BY--SA--4.0-31393F?style=flat&logo=creativecommons&logoColor=black&labelColor=white)

This sets up an Airflow infrastructure in Docker that mirrors, as close as possible, Airflow deployments on Kubernetes (via Helm charts), making it easier to develop locally while keeping production parity.

It also uses the same base image as [GCP Composer for Airflow](https://docs.cloud.google.com/composer/docs/composer-versions), ensuring compatibility if you plan to deploy to Google Cloud Platform.


## Getting Started

**1.** Start setting up the infrastructure in Docker with:
```shell
docker compose up --build -d
```

The default [compose.yaml](./compose.yaml) is a symlink to the **LocalExecutor**.

Alternatively you can run it with the **CeleryExecutor** with:

```shell
docker compose -f compose.celery.yaml up --build -d
```

**2.** Airflow WebUI can be accessed at:
```shell
open http://localhost:8080
```


## TODO's:
- [x] PEP-517: Packaging and dependency management with `uv`
- [x] Run Airflow DAGs on Docker
- [x] Configure Airflow to use GCS as XCOM's backend
- [ ] Configure Airflow to use AWS S3 as XCOM's backend
- [ ] Build Airflow DAGs to ingest Web CSV to Postgres
- [ ] Build Airflow DAGs to ingest Web CSV to Object Storage (GCS)
- [ ] Build Airflow DAGs to ingest Web CSV to Postgres with [TaskFlow API](https://airflow.apache.org/docs/apache-airflow/stable/tutorial/taskflow.html)
- [ ] Deploy [Airflow to Kubernetes with Helm](https://airflow.apache.org/docs/helm-chart/stable/index.html)
- [ ] Run Airflow DAGs on Kubernetes using the [KubernetesPodOperator](https://airflow.apache.org/docs/apache-airflow-providers-cncf-kubernetes/stable/operators.html)
- [x] Code format/lint with `ruff`
