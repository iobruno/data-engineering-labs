# Batch processing with PySpark

![Python](https://img.shields.io/badge/Python-3.14_|_3.13_|_3.12-4B8BBE.svg?style=flat&logo=python&logoColor=FFD43B&labelColor=306998)
[![JDK](https://img.shields.io/badge/JDK-21_|_17-1076C6?style=flat&logo=openjdk&logoColor=FFFFFF&labelColor=1076C6)](https://sdkman.io/)
[![PySpark](https://img.shields.io/badge/PySpark-3.5-262A38?style=flat-square&logo=apachespark&logoColor=E36B22&labelColor=262A38)](https://spark.apache.org/docs/latest/api/python/user_guide)
[![uv](https://img.shields.io/badge/astral/uv-261230?style=flat&logo=uv&logoColor=DE5FE9&labelColor=261230)](https://docs.astral.sh/uv/getting-started/installation/)
[![SDKMan](https://img.shields.io/badge/SDKMan-1076C6?style=flat&logo=openjdk&logoColor=FFFFFF&labelColor=1076C6)](https://sdkman.io/)
[![Docker](https://img.shields.io/badge/Docker-329DEE?style=flat&logo=docker&logoColor=white&labelColor=329DEE)](https://docs.docker.com/get-docker/)

![License](https://img.shields.io/badge/license-CC--BY--SA--4.0-31393F?style=flat&logo=creativecommons&logoColor=black&labelColor=white)

PySpark Playground for NY Taxi Tripdata Batch Processing Pipeline

```
Welcome to
      ____              __
     / __/__  ___ _____/ /__
    _\ \/ _ \/ _ `/ __/  '_/
   /__ / .__/\_,_/_/ /_/\_\   version 3.5.3
      /_/

Using Python version 3.11.11 (main, Jan 14 2025 23:36:41)
Spark context Web UI available at http://192.168.15.29:4040
Spark context available as 'sc' (master = local[*], app id = local-1738438879580).
SparkSession available as 'spark'.
```


## Getting Started

**1.** Install JDK 21 or 17 (earlier versions are deprecated) for Spark 4.x with [SDKMan](https://sdkman.io/):
```shell
sdk i java 21.0.10-librca
sdk i java 17.0.18-librca
```

**2.** Install dependencies from pyproject.toml and activate the created virtualenv:
```shell
uv sync && source .venv/bin/activate
```

**3.** (Optional) Install pre-commit:
```shell
brew install pre-commit

# From root folder where `.pre-commit-config.yaml` is located, run:
pre-commit install
```

**4.** Spin up the Spark Cluster with:
```shell
docker compose -f ../compose.yaml up -d
```

## TODO's:
- [x] PEP-517: Packaging and dependency management with `uv`
- [x] Code format/lint with Ruff
- [X] Set up a Jupyter Playground for PySpark
- [X] Enable Spark to read from Google Cloud Storage
- [ ] Enable Spark to read from AWS S3
- [ ] Submit a PySpark job to the Google Dataproc
- [ ] Deploy [Spark to Kubernetes with Helm](https://github.com/GoogleCloudPlatform/spark-on-k8s-operator) with [minikube](https://minikube.sigs.k8s.io/docs/start/) or [kind](https://kind.sigs.k8s.io/)
- [ ] Submit a PySpark job to the K8s Spark Cluster
