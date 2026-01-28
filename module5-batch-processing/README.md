# Batch processing with Spark

![Python](https://img.shields.io/badge/Python-3.13_|_3.12-4B8BBE.svg?style=flat&logo=python&logoColor=FFD43B&labelColor=306998)
[![PySpark](https://img.shields.io/badge/PySpark-4.0-262A38?style=flat-square&logo=apachespark&logoColor=E36B22&labelColor=262A38)](https://spark.apache.org/docs/latest/api/python/user_guide)
![Scala](https://img.shields.io/badge/Scala-2.13-262A38?style=flat-square&logo=scala&logoColor=E03E3C&labelColor=262A38)
[![Kotlin](https://img.shields.io/badge/Kotlin_SparkAPI-2.x-262A38?style=flat-square&logo=kotlin&logoColor=603DC0&labelColor=262A38)](https://github.com/Kotlin/kotlin-spark-api)
[![JDK](https://img.shields.io/badge/JDK-21_|_17-35667C?style=flat&logo=openjdk&logoColor=FFFFFF&labelColor=1D213B)](https://sdkman.io/)
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

**1.** Spin up the Spark Cluster
```shell
docker compose up -d
```

**2.** Refer to the specific implementations for docs on how to run the pipeline:

- [Kotlin](./kotlin/)
- [Scala](./scala/)
- [PySpark](./pyspark/)
