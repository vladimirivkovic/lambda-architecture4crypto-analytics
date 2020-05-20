import os
import time
import json

from hexbytes import HexBytes
from web3.auto import w3
from kafka import KafkaProducer
import kafka.errors

KAFKA_BROKER = os.environ["KAFKA_BROKER"]
TOPIC = "eth-block"
START_DELAY = 30


class HexJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, HexBytes):
            return obj.hex()
        return super().default(obj)


def connect_to_kafka():
    while True:
        try:
            producer = KafkaProducer(bootstrap_servers=KAFKA_BROKER.split(","))
            print("Connected to Kafka!")
            return producer
        except kafka.errors.NoBrokersAvailable as e:
            print(e)
            time.sleep(3)


def handle_event(event, kafka_producer):
    for _ in range(5):
        try:
            block = w3.eth.getBlock(event)
            break
        except:
            print("getBlock error")
            time.sleep(1)
    else:
        return

    block_dict = dict(block)
    block_json = json.dumps(block_dict, cls=HexJsonEncoder)
    print(block_dict["hash"])
    kafka_producer.send(TOPIC, key=bytes(str(block_dict["hash"]), "utf-8"), value=bytes(block_json, "utf-8"))


def log_loop(event_filter, poll_interval, kafka_producer):
    while True:
        for event in event_filter.get_new_entries():
            handle_event(event, kafka_producer)
        time.sleep(poll_interval)


def main():
    print("Starting Ethereum listener ...")
    producer = connect_to_kafka()
    time.sleep(START_DELAY)
    block_filter = w3.eth.filter('latest')
    log_loop(block_filter, 2, producer)


if __name__ == "__main__":
    main()
