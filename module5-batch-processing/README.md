# Batch processing with Spark

![Python](https://img.shields.io/badge/Python-3.14_|_3.13_|_3.12-4B8BBE.svg?style=flat&logo=python&logoColor=FFD43B&labelColor=306998)
[![PySpark](https://img.shields.io/badge/PySpark-4.2-262A38?style=flat-square&logo=apachespark&logoColor=E36B22&labelColor=262A38)](https://spark.apache.org/docs/4.2.0/api/python/user_guide)
[![Scala](https://img.shields.io/badge/Scala-2.13-262A38?style=flat-square&logo=scala&logoColor=E03E3C&labelColor=262A38)](https://sdkman.io/usage/)
[![JDK](https://img.shields.io/badge/JDK-25_|_21_|_17-35667C?style=flat&logo=openjdk&logoColor=FFFFFF&labelColor=1D213B)](https://sdkman.io/usage/)


## Getting Started

### Spin up the Spark Cluster 4.2
```shell
docker compose up -d
```

Refer to [PySpark 4.x](./pyspark-4.x/README.md) for how to run the pipeline

### Spin up the Spark Cluster 3.5
```shell
docker compose -f compose.spark-3.5-standalone.yaml up -d
```

Refer to [PySpark 3.5](./pyspark-3.x/README.md) for how to run the pipeline
