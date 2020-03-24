from kafka import KafkaConsumer
import kafka.errors
from hdfs import InsecureClient
import os
import sys
import time
import json


BLOCKS_PATH = '/blocks'


def connect_to_hdfs():
    return InsecureClient(os.environ['HDFS_HOST'], user='root')


def upload_to_hdfs(hdfs, content, base_dir, format):
    filename = base_dir + BLOCKS_PATH + "-" + str(time.time()).split('.')[0]
    print("writing " + filename + " ...")
    hdfs.write(filename + format, data=content, encoding="utf-8")


def handle_msg(hdfs, msg, base_dir, max_blocks):
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
        handle_msg(hdfs, msg, base_dir)