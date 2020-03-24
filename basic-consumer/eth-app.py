from kafka import KafkaConsumer
import kafka.errors
from hdfs import InsecureClient
import os
import sys
import time
import json

TOPIC = 'eth-block'
MAX_BLOCKS = 25
ETH_DIR = '/user/data/ethereum'
BLOCKS_PATH = '/blocks'

START_DELAY = 60
SLEEP_INTERVAL = 3

blocks = []


def connect_to_hdfs():
    return InsecureClient(os.environ['HDFS_HOST'], user='root')


def upload_to_hdfs(hdfs, content, base_dir, format):
    filename = base_dir + BLOCKS_PATH + "-" + str(time.time()).split('.')[0]
    print("writing " + filename + " ...")
    hdfs.write(filename + format, data=content, encoding="utf-8")


def handle_msg(msg, base_dir):
    global blocks
    try:
        blocks.append(json.loads(msg.value))
    except Exception as e: 
        print(e)

    if (len(blocks) >= MAX_BLOCKS):
        upload_to_hdfs(hdfs, json.dumps(blocks), base_dir, ".json")
        blocks = []


def consume(hdfs, consumer, base_dir):
    for msg in consumer:
        handle_msg(msg, base_dir)


def connect_to_kafka():
    while True:
        try:
            consumer = KafkaConsumer(
                TOPIC, bootstrap_servers=os.environ['KAFKA_BROKER'], group_id="hdfs-consumer")
            print("Connected to Kafka!")
            return consumer
        except kafka.errors.NoBrokersAvailable as e:
            print(e)
            time.sleep(SLEEP_INTERVAL)


if __name__ == '__main__':
    time.sleep(START_DELAY)

    hdfs = connect_to_hdfs()
    # hdfs.delete(ETH_DIR, recursive=True)
    try:
        hdfs.makedirs(ETH_DIR)
    except:
        pass

    consumer = connect_to_kafka()
    consume(hdfs, consumer, ETH_DIR)