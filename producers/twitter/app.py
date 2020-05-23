import tweepy
import os
import json
import time
from kafka import KafkaProducer
import kafka.errors

KAFKA_BROKER = os.environ["KAFKA_BROKER"]
TOPIC = "tweets"
START_DELAY = 30

API_KEY = os.environ["API_KEY"]
API_SECRET_KEY = os.environ["API_SECRET_KEY"]

ACCESS_TOKEN = os.environ["ACCESS_TOKEN"]
ACCESS_TOKEN_SECRET = os.environ["ACCESS_TOKEN_SECRET"]

TRACKS = os.environ["TRACKS"].split(",")  # ["bitcoin", "ethereum"]

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


class Listener(tweepy.StreamListener):

    def __init__(self, track):
        self.track = track

    def on_data(self, data):
        t = json.loads(data)
        producer.send(f"{TOPIC}-{self.track}", key=bytes(
            str(t["id"]), "utf-8"), value=bytes(data, "utf-8"))
        return True

    def on_error(self, status):
        print(status)


def main():
    global producer
    print("Starting Twitter listener ...")
    producer = connect_to_kafka()
    time.sleep(START_DELAY)

    auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    for t in TRACKS:
        twitterStream = tweepy.Stream(auth, Listener(t))
        twitterStream.filter(track=[t], is_async=True)


if __name__ == "__main__":
    main()
