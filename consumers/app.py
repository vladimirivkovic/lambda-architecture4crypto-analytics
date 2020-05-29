import os
import sys
import time
import json

from kafka import KafkaConsumer
import kafka.errors
from hdfs import InsecureClient
from hdfs.ext.avro import AvroWriter
from fastavro import parse_schema

TOPIC = os.environ['TOPIC']
MAX_RECORDS = int(os.environ['MAX_RECORDS'])
BASE_DIR = f'/user/data/{TOPIC}/'
SCHEMA_FILE = os.environ['SCHEMA_FILE']
FILE_NAME = 'data'

START_DELAY = 60
SLEEP_INTERVAL = 3

with open(SCHEMA_FILE) as schema_file:
    schema = json.load(schema_file)
parsed_schema = parse_schema(schema)


def convert(data):
    if isinstance(data, bytes):
        return data.decode('utf-8')
    if isinstance(data, dict):
        return dict(map(convert, data.items()))
    if isinstance(data, tuple):
        return map(convert, data)
    return data


def connect_to_hdfs():
    return InsecureClient(os.environ['HDFS_HOST'], user='root')


def upload_to_hdfs(hdfs, records):
    global first
    print('saving to AVRO ...')
    # print(records)

    with AvroWriter(hdfs, f'{BASE_DIR}{FILE_NAME}-{round(time.time())}.avro', schema=parsed_schema) as writer:
        for record in records:
            try:
                writer.write(record)
            except:
                continue
    first = False


def handle_msg(msg, records):
    try:
        records.append(json.loads(msg.value))
    except Exception as e:
        print(e)

    if (len(records) >= MAX_RECORDS):
        upload_to_hdfs(hdfs, records)
        records = []

    return records


def consume(hdfs, consumer):
    records = []
    for msg in consumer:
        records = handle_msg(msg, records)


def connect_to_kafka():
    while True:
        try:
            consumer = KafkaConsumer(
                TOPIC, bootstrap_servers=os.environ['KAFKA_BROKER'], group_id="hdfs-consumer")
            print('Connected to Kafka!')
            return consumer
        except kafka.errors.NoBrokersAvailable as e:
            print(e)
            time.sleep(SLEEP_INTERVAL)


if __name__ == '__main__':
    time.sleep(START_DELAY)
    print(f'Starting {TOPIC} consumer ...')

    hdfs = connect_to_hdfs()
    try:
        hdfs.makedirs(BASE_DIR)
    except:
        pass

    consumer = connect_to_kafka()
    consume(hdfs, consumer)
