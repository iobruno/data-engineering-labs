# Batch processing with PySpark

![Python](https://img.shields.io/badge/Python-3.13_|_3.12-4B8BBE.svg?style=flat&logo=python&logoColor=FFD43B&labelColor=306998)
[![PySpark](https://img.shields.io/badge/PySpark-4.0-262A38?style=flat-square&logo=apachespark&logoColor=E36B22&labelColor=262A38)](https://spark.apache.org/docs/latest/api/python/user_guide)
[![JDK](https://img.shields.io/badge/JDK-21_|_17-35667C?style=flat&logo=openjdk&logoColor=FFFFFF&labelColor=1D213B)](https://sdkman.io/)
[![SDKMan](https://img.shields.io/badge/SDKMan-35667C?style=flat&logo=openjdk&logoColor=FFFFFF&labelColor=1D213B)](https://sdkman.io/)
[![uv](https://img.shields.io/badge/astral/uv-261230?style=flat&logo=uv&logoColor=DE5FE9&labelColor=261230)](https://docs.astral.sh/uv/getting-started/installation/)
[![Docker](https://img.shields.io/badge/Docker-329DEE?style=flat&logo=docker&logoColor=white&labelColor=329DEE)](https://docs.docker.com/get-docker/)

![License](https://img.shields.io/badge/license-CC--BY--SA--4.0-31393F?style=flat&logo=creativecommons&logoColor=black&labelColor=white)

```
Welcome to
      ____              __
     / __/__  ___ _____/ /__
    _\ \/ _ \/ _ `/ __/  '_/
   /__ / .__/\_,_/_/ /_/\_\   version 4.0.1
      /_/

Using Python version 3.14.2 (main, Jan 14 2026 23:37:46)
Spark context Web UI available at http://192.168.15.5:4043
Spark context available as 'sc' (master = local[*], app id = local-1769554629678).
SparkSession available as 'spark'.
Cmd click to launch VS Code Native REPL
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
- [x] Spin up a Spark Cluster in Standalone mode w/ Spark Connect
- [x] `submit` a PySpark Job to the cluster with Spark Connect
- [x] `spark-submit` a PySpark Job to the cluster in `--deploy-mode client`
- [x] Enable Spark to read from Google Cloud Storage
- [ ] Submit a PySpark job to Google Dataproc
- [ ] Enable Spark to read from AWS S3
- [ ] Deploy [Spark to Kubernetes with Helm](https://github.com/GoogleCloudPlatform/spark-on-k8s-operator) with [minikube](https://minikube.sigs.k8s.io/docs/start/) or [kind](https://kind.sigs.k8s.io/)
- [ ] Submit a PySpark job to the K8s Spark Cluster
