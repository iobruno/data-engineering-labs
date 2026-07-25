# Workflow orchestration with Airflow 3.x

![Python](https://img.shields.io/badge/Python-3.11-4B8BBE.svg?style=flat&logo=python&logoColor=FFD43B&labelColor=306998)
[![Airflow](https://img.shields.io/badge/Airflow-3.1-007CEE?style=flat&logo=apacheairflow&logoColor=white&labelColor=14193A)](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/taskflow.html)
[![Pandas](https://img.shields.io/badge/pandas-150458?style=flat&logo=pandas&logoColor=E70488&labelColor=150458)](https://pandas.pydata.org/docs/user_guide/)
[![uv](https://img.shields.io/badge/astral/uv-261230?style=flat&logo=uv&logoColor=DE5FE9&labelColor=261230)](https://docs.astral.sh/uv/getting-started/installation/)
[![Docker](https://img.shields.io/badge/Docker-329DEE?style=flat&logo=docker&logoColor=white&labelColor=329DEE)](https://docs.docker.com/get-docker/)

![License](https://img.shields.io/badge/license-CC--BY--SA--4.0-31393F?style=flat&logo=creativecommons&logoColor=black&labelColor=white)

This mirrors the [Airflow 2.x](../airflow-2.x/) setup in this same module, but on Airflow 3.1, which introduces a few architectural changes:

- The **webserver** is replaced by the **API server** (`airflow api-server`), serving both the new UI and the stable REST API.
- DAG parsing is decoupled from the scheduler into its own **DAG processor** service (`airflow dag-processor`), which is now required regardless of executor.
- Task execution talks to the API server over the new **Task Execution API** (`AIRFLOW__CORE__EXECUTION_API_SERVER_URL`), rather than hitting the metadata DB directly.
- Auth is now pluggable via **Auth Managers**; the default is the `SimpleAuthManager`. This setup explicitly configures the **FAB Auth Manager** (`apache-airflow-providers-fab`) to preserve the same `airflow`/`airflow` basic-auth login used in the 2.x setup.


## Migrating to Airflow 3.x

Service-by-service comparison against the [Airflow 2.x](../airflow-2.x/) compose files:

| Airflow 2.x       | Airflow 3.x               | What it is                                                                                                                                                                             |
|-------------------|---------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `airflow-web`     | `airflow-api-server`      | Serves the UI and the REST API. Renamed because it's no longer just a webserver: task processes now call into it directly over the new Task Execution API instead of hitting the metadata DB. |
| *(none — parsed inside the scheduler)* | `airflow-dag-processor`  | New, required regardless of executor. DAG file parsing used to run inside the scheduler process; it's now its own service, so DAG code no longer needs to be readable by the scheduler at all. |
| `airflow-scheduler` | `airflow-scheduler`     | Same job: evaluates schedules and queues task instances. No longer parses DAG files itself (moved to `airflow-dag-processor`); under LocalExecutor it also calls the Task Execution API to run tasks in-process. |
| `airflow-worker`  | `airflow-worker`          | CeleryExecutor only. Same job: pulls queued tasks off the broker and executes them. Now talks to `airflow-api-server` over the Task Execution API instead of the metadata DB directly. |
| `airflow-triggerer` | `airflow-triggerer`     | Unchanged. Runs deferrable/async tasks in a single event loop.                                                                                                                          |
| `airflow-flower`  | `airflow-flower`          | CeleryExecutor only. Unchanged — Celery task/worker monitoring UI.                                                                                                                     |
| `airflow-init`    | `airflow-init`            | Same one-shot job: migrates the metadata DB and bootstraps the admin user. In 3.x every other service also syncs FAB permissions on its own startup, so they now explicitly wait for `airflow-init` to finish first (`depends_on: service_completed_successfully`) to avoid racing its inserts on a fresh DB. |
| `airflow-metastore` | `airflow-metastore`     | Unchanged. Postgres backing Airflow's own metadata DB.                                                                                                                                 |
| `airflow-redis`   | `airflow-redis`           | CeleryExecutor only. Unchanged — Celery broker.                                                                                                                                        |
| `tlc-db`          | `tlc-db`                  | Unchanged. Target Postgres sink that DAGs ingest NYC TLC data into.                                                                                                                     |


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
