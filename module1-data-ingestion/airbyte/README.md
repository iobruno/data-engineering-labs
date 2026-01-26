# Airbyte SDK / CDK Labs

![Python](https://img.shields.io/badge/Python-3.14_|_3.13_|_3.12-4B8BBE.svg?style=flat&logo=python&logoColor=FFD43B&labelColor=306998)
[![Airbyte](https://img.shields.io/badge/Airbyte-2.0.19-007CEE?style=flat&logo=airbyte&logoColor=5F5DFF&labelColor=14193A)](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/taskflow.html)
[![Docker](https://img.shields.io/badge/Docker-329DEE?style=flat&logo=docker&logoColor=white&labelColor=329DEE)](https://docs.docker.com/get-docker/)

Docker Compose support is [officially deprecated and no longer supported](https://github.com/airbytehq/airbyte/discussions/40599). Airbyte now uses [abctl](https://docs.airbyte.com/platform/1.8/deploying-airbyte/abctl) - a CLI that manages local instances of Airbyte using [KinD](https://kind.sigs.k8s.io/)


## Pre-requisites
- Docker Desktop


## Getting started (Local env)

1. Install abctl tool:
```shell
curl -LsfS https://get.airbyte.com | bash -
```

```shell
abctl local install
```

2. Get your credentials with:
```shell
abctl local credentials
```

**3.** Airbyte WebUI can be accessed at:
```shell
open http://localhost:8000
```


## Custom Connectors
- T.B.D.


## TODO
- [ ] Spin-up Airbyte with `abctl`
- [ ] Get familiar with [Airbyte API Python SDK](https://github.com/airbytehq/airbyte-api-python-sdk)
- [ ] Configure Source/Destinations/Connections with [Airbyte Terraform provider](https://docs.airbyte.com/platform/1.8/terraform-documentation)
- [ ] Create a Custom Source Connector using [Python CDK](https://docs.airbyte.com/platform/connector-development/cdk-python/)
