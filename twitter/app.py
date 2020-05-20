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

    def on_data(self, data):
        t = json.loads(data)
        producer.send(TOPIC, key=bytes(
            str(t["id"]), "utf-8"), value=bytes(data, "utf-8"))
        #
        # print("\n\n\n")
        # print(t["created_at"])
        # print(t["id"])
        # print(t["in_reply_to_status_id"])
        # print(t["in_reply_to_user_id"])
        # print(t["in_reply_to_screen_name"])
        # print(t["user"]["id"])
        # print(t["user"]["screen_name"])
        # print(t["user"]["followers_count"])
        # print(t["is_quote_status"])
        # print(t["quote_count"])
        # print(t["reply_count"])
        # print(t["retweet_count"])
        # print(t["favorite_count"])
        # print(t["entities"]["hashtags"])
        # print(t["lang"])
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

    twitterStream = tweepy.Stream(auth, Listener())
    twitterStream.filter(track=["bitcoin"])


if __name__ == "__main__":
    main()
