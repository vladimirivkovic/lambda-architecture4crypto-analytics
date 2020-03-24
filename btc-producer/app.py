from flask import Flask
import os
import socket
import time
import json
from decimal import Decimal

from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
from kafka import KafkaProducer
import kafka.errors

rpc_user = 'foo'
rpc_password = 'qDDZdeQ5vw9XXFeVnXT4PZ--tGN2xNjjR4nrtyszZx0='
rpc_port = "8332"

KAFKA_BROKER = os.environ["KAFKA_BROKER"]
TOPIC = "btc-block"


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)


def connect_to_kafka():
    while True:
        try:
            producer = KafkaProducer(bootstrap_servers=KAFKA_BROKER.split(","))
            print("Connected to Kafka!")
            return producer
        except kafka.errors.NoBrokersAvailable as e:
            print(e)
            time.sleep(3)


producer = connect_to_kafka()
app = Flask(__name__)


@app.route("/btc/<block>")
def btc_block(block):
    rpc_connection = AuthServiceProxy(
        "http://%s:%s@bitcoin-node:%s" % (rpc_user, rpc_password, rpc_port), timeout=120)
    block_dict = rpc_connection.getblock(block)
    print("new block_json")
    producer.send(TOPIC, key=bytes(str(block), "utf-8"),
                  value=bytes(json.dumps(block_dict, cls=DecimalEncoder), "utf-8"))

    return "OK"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
