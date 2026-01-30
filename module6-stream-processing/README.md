# Stream processing with Kafka & ksqlDB

[![Kafka](https://img.shields.io/badge/Confluent_Platform-8.1-141414?style=flat&logo=apachekafka&logoColor=white&labelColor=141414)](https://docs.confluent.io/platform/current/)
[![Docker](https://img.shields.io/badge/Docker-329DEE?style=flat&logo=docker&logoColor=white&labelColor=329DEE)](https://docs.docker.com/get-docker/)

![License](https://img.shields.io/badge/license-CC--BY--SA--4.0-31393F?style=flat&logo=creativecommons&logoColor=black&labelColor=white)

This submodule focuses on various approaches for stream processing, such as:

- [Kotlin](kotlin/): Producing and Consuming messages from/to Kafka with Kotlin/Java
- [ksqlDB](ksqldb/): Stream Processing with ksqlDB (Kafka Streams)


## Getting Started

**1.** Spin up Kafka Broker with one of the following options:

1.1. Kafka Cluster (Single-broker) with KRaft:
```shell
docker compose up -d
```

1.2. Kafka Cluster (Multi-broker) with KRaft:
```shell
docker compose -f compose.kraft-multi-broker.yaml up -d
```

1.3. Kafka Cluster (Multi-broker) with Zookeeper:
```shell
docker compose -f compose.zookeeper-multi-broker.yaml up -d
```

1.4. Redpanda:
```shell
docker compose -f compose.redpanda.yaml up -d
```

**2.** Access Conduktor Web UI for Kafka
```shell
open http://localhost:8080
```


## TODO's:
- [x] Single-broker Kafka Cluster (with KRaft)
- [x] Multi-broker Kafka Cluster (with KRaft)
- [x] Multi-broker Kafka Cluster (with Zookeeper)
- [x] Confluent Schema Registry
- [x] Confluent Rest Proxy
- [x] ksqlDB Server and CLI
- [x] Kafka Admin UI: `Conduktor Console`
- [ ] Deploy Kafka Cluster on Kubernetes using Helm Charts
