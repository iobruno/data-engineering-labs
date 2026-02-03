# Stream processing with Kafka, ksqlDB and Kotlin

[![Kafka](https://img.shields.io/badge/Confluent_Platform-8.1-141414?style=flat&logo=apachekafka&logoColor=white&labelColor=141414)](https://docs.confluent.io/platform/current/)
[![Kotlin](https://img.shields.io/badge/Kotlin-2.2-262A38?style=flat-square&logo=kotlin&logoColor=603DC0&labelColor=262A38)](https://github.com/Kotlin/kotlin-spark-api)
[![JDK](https://img.shields.io/badge/JDK-21_|_17-35667C?style=flat&logo=openjdk&logoColor=FFFFFF&labelColor=1D213B)](https://sdkman.io/)
[![Gradle](https://img.shields.io/badge/gradle-9.3-31ADC3?style=flat&logo=gradle&logoColor=white&labelColor=011E24)](https://gradle.org/releases/)
[![Docker](https://img.shields.io/badge/Docker-329DEE?style=flat&logo=docker&logoColor=white&labelColor=329DEE)](https://docs.docker.com/get-docker/)

![License](https://img.shields.io/badge/license-CC--BY--SA--4.0-31393F?style=flat&logo=creativecommons&logoColor=black&labelColor=white)

Experiment with stream processing using `Kotlin`, `Kafka`, and `ksqlDB`, providing a playground for seamless data integration and analysis


## Getting Started

**1.** Install JDK 21 or 17 (earlier versions are deprecated) for Spark 4.x with [SDKMan](https://sdkman.io/):
```shell
sdk i java 21.0.10-librca
sdk i java 17.0.18-librca
```

**2.** (Optional) Install pre-commit:
```shell
brew install pre-commit

# From root folder where `.pre-commit-config.yaml` is located, run:
pre-commit install
```

**3.** Build and generate the application artifact:
```shell
./gradlew clean shadowJar
```

**4.** Start Kafka, Schema Registry and others from the parent directory:
```shell
docker compose up -d
```

**5.** Run the application with and check the subcommands:
```shell
java -jar build/libs/kotlin-sp-2.0.jar
```
```text
Commands:
  help      Display help information about the specified command.
  producer  Parse data from source dataset and publish as JSON to Kafka
  consumer  Subscribe and consume records from Kafka topic
```

**5.1.** CLI for ProducerApp
```shell
 java -jar build/libs/kotlin-sp-2.0.jar producer
```
```text
Parse data from source dataset and publish as JSON to Kafka
Commands:
  green   Process GreenTaxiDTO data from CSV file and publish to Kafka topic
  yellow  Process YellowTaxiDTO data from CSV file and publish to Kafka topic
  fhv     Process FhvTaxiDTO data from CSV file and publish to Kafka topic
```

```shell
java -jar build/libs/kotlin-sp-2.0.jar producer [green|yellow|fhv]
```
```text
Process [GreenTaxiDTO|YellowTaxiDTO|FhvTaxiDTO] data from CSV file and publish to Kafka topic
  -i, --csv-file=<csvFilePath>
                        CSV file path
  -t, --topic=<topic>   Target Kafka topic for records
```

**5.2.** CLI for ConsumerApp
```shell
java -jar build/libs/kotlin-sp-2.0.jar consumer
```
```text
Subscribe and consume records from Kafka topic
Commands:
  green   Deserialize ConsumerRecords from source Kafka topic to GreenTaxiDTO
  yellow  Deserialize ConsumerRecords from source Kafka topic to YellowTaxiDTO
  fhv     Deserialize ConsumerRecords from source Kafka topic to FhvTaxiDTO
```

```shell
java -jar build/libs/kotlin-sp-2.0.jar consumer [green|yellow|fhv]
```
```text
Deserialize ConsumerRecords from source Kafka topic to [GreenTaxiDTO|YellowTaxiDTO|FhvTaxiDTO]
  -g, --consumer-group=<consumerGroup>
                        Consumer group to subscribe to the Source kafka topic
  -t, --topic=<topic>   Source Kafka topic for records
```

## TODO's:
- [x] Set up an environment for Kotlin, Kafka Client and KafkaStreams
- [x] Set up a Schema Registry
- [x] Build a Cli Application for Producer and Consumer
- [x] Explore serialization with `JSON`
- [ ] Explore serialization with `Protobuf`
- [x] Adds support to Native Image builds (GraalVM)
- [x] Static code analysis with [detekt](https://detekt.dev/)