# Batch processing with PySpark 4.x

![Python](https://img.shields.io/badge/Python-3.13_|_3.12-4B8BBE.svg?style=flat&logo=python&logoColor=FFD43B&labelColor=306998)
[![PySpark](https://img.shields.io/badge/PySpark-4.x-262A38?style=flat-square&logo=apachespark&logoColor=E36B22&labelColor=262A38)](https://spark.apache.org/docs/4.0.2/api/python/user_guide)
[![Hadoop](https://img.shields.io/badge/Hadoop-3.4.x-262A38?style=flat-square&logo=apachehadoop&logoColor=FDEE21&labelColor=262A38)](https://spark.apache.org/docs/4.0.2/api/python/user_guide)
[![Scala](https://img.shields.io/badge/Scala-2.13-262A38?style=flat-square&logo=scala&logoColor=E03E3C&labelColor=262A38)](https://sdkman.io/usage/)
[![JDK](https://img.shields.io/badge/JDK-21_|_17-35667C?style=flat&logo=openjdk&logoColor=FFFFFF&labelColor=1D213B)](https://sdkman.io/usage/)
[![uv](https://img.shields.io/badge/astral/uv-261230?style=flat&logo=uv&logoColor=DE5FE9&labelColor=261230)](https://docs.astral.sh/uv/getting-started/installation/)
[![Docker](https://img.shields.io/badge/Docker-329DEE?style=flat&logo=docker&logoColor=white&labelColor=329DEE)](https://docs.docker.com/get-docker/)

![License](https://img.shields.io/badge/license-CC--BY--SA--4.0-31393F?style=flat&logo=creativecommons&logoColor=black&labelColor=white)


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

**5.** Spark Web UI
- Spark Master Web UI can be accessed at [http://localhost:4040](http://localhost:4040)
- Spark History Server can be accessed at [http://localhost:18080](http://localhost:18080)


## Spark-submit Application

### Local (Spark Driver running on local machine)

With `--deploy-mode client` (default), the Spark Driver runs locally and doesn't pick up [spark-4.0-standalone.conf](../compose.spark-4.0-standalone.yaml), so the `--conf spark.hadoop.*` options must be set explicitly.

```shell
spark-submit \
    --master spark://localhost:7077 \
    --packages "com.google.cloud.bigdataoss:gcs-connector-4.0.2-shaded.jar" \
    --conf spark.eventLog.enabled=true \
    --conf spark.eventLog.dir=file://$(pwd)/../logs/ \
    --conf spark.hadoop.fs.gs.impl=com.google.cloud.hadoop.fs.gcs.GoogleHadoopFileSystem \
    --conf spark.hadoop.fs.AbstractFileSystem.gs.impl=com.google.cloud.hadoop.fs.gcs.GoogleHadoopFS \
    fhv_zones_gcs.py
```


## Compatibility Matrix for GCS

### Spark 4.x, Hadoop, and GCS Connector

| Spark | Bundled Hadoop | GCS Connector | Status |
|-------|---------------|---------------|--------|
| 4.0.x | 3.4.1 | `gcs-connector-4.0.x-shaded.jar` | ✅ Recommended. Built against Hadoop 3.4.2. |
| 4.0.x | 3.4.1 | `gcs-connector-3.1.x-shaded.jar` | ⚠️ Compatible, but targets Hadoop 3.3.5. |
| 4.0.x | 3.4.1 | `gcs-connector-hadoop3-2.2.x-shaded.jar` | ⚠️ Works, but uses legacy auth config and misses `openFile` optimization. |
| 4.0.x | 3.4.1 | `gcs-connector-hadoop2-*-shaded.jar` | ❌ Do not use. Hadoop 2.x only. |

### Auth Configuration

The auth properties changed in GCS Connector 3.0.0:

| Connector | Auth Type | Keyfile Path |
|-----------|-----------|-------------|
| 4.x / 3.x | `google.cloud.auth.type=SERVICE_ACCOUNT_JSON_KEYFILE` | `google.cloud.auth.service.account.json.keyfile` |
| 2.2.x | `fs.gs.auth.service.account.enable=true` | `fs.gs.auth.service.account.json.keyfile` |

> **Note:** In Spark config files, all Hadoop properties must be prefixed with `spark.hadoop.`.
> The `fs.gs.impl` and `fs.AbstractFileSystem.gs.impl` properties are unchanged across all versions.

### Breaking Changes

| Version | Change |
|---------|--------|
| 4.0.0 | Added `listStatusStartingFrom` API. Bumped Hadoop target to 3.4.2. |
| 3.0.0 | Dropped Hadoop 2.x. Moved auth from `fs.gs.auth.*` to `google.cloud.auth.*`. Added `FileSystem.openFile` (requires Hadoop 3.4+). Merged output streams into `FLUSHABLE_COMPOSITE`. Removed Cooperative Locking. |


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
