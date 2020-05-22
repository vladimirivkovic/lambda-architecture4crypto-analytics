import os
import websocket
import json
import time
from kafka import KafkaProducer
import kafka.errors

try:
    import thread
except ImportError:
    import _thread as thread
import time

KAFKA_BROKER = os.environ["KAFKA_BROKER"]
TOPIC = "exchange-rates"
START_DELAY = 30

WS_SERVER = 'wss://streamer.cryptocompare.com/v2'
SUB_MSG = '{ \
    "action": "SubAdd", \
    "subs": ["5~CCCAGG~BTC~USD", "5~CCCAGG~ETH~USD"] \
}'
AUTH_HEADER = "Authorization: Apikey " + os.environ["API_KEY"]


producer = None


def connect_to_kafka():
    while True:
        try:
            producer = KafkaProducer(bootstrap_servers=KAFKA_BROKER.split(","))
            print("Connected to Kafka!")
            return producer
        except kafka.errors.NoBrokersAvailable as e:
            print(e)
            time.sleep(3)


def on_message(ws, message):
    msg = json.loads(message)
    if msg["TYPE"] == "5":
        producer.send(TOPIC, key=bytes(
            msg["FROMSYMBOL"], "utf-8"), value=bytes(message, "utf-8"))


def on_error(ws, error):
    print(error)


def on_close(ws):
    print("### closed ###")


def on_open(ws):
    def run(*args):
        ws.send(SUB_MSG)
    thread.start_new_thread(run, ())


def main():
    global producer
    print("Starting Exchange Rate listener ...")
    producer = connect_to_kafka()
    time.sleep(START_DELAY)

    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(WS_SERVER,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close,
                                header=[AUTH_HEADER])
    ws.on_open = on_open
    ws.run_forever()


if __name__ == "__main__":
    main()
