#!/bin/sh

export HADOOP_VERSION="2.0.0-hadoop3.2.1-java8"
export SPARK_VERSION="2.4.0-hadoop3.1"

docker-compose -f docker-compose.yml \
    -f producers/docker-compose.yml \
    -f consumers/docker-compose.yml \
    -f docker-compose-kafka.yml \
    -f docker-compose-hdfs.yml \
    -f docker-compose-spark.yml \
    -f docker-compose-druid.yml \
    up --build