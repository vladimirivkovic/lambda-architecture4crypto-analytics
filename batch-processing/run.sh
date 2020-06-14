#!/bin/bash

docker cp . spark-master:/home

docker exec -it spark-master bash -c \
    "/spark/bin/spark-shell --packages org.apache.spark:spark-avro_2.11:2.4.5 \
    -i /home/ethereum_stats.scala < /home/empty.scala"