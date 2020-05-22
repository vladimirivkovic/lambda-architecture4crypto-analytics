#!/usr/bin/python3

import os
import time
import praw
import json
from kafka import KafkaProducer
import kafka.errors

SUBREDDITS = os.environ["SUBREDDITS"].split(",")

KAFKA_BROKER = os.environ["KAFKA_BROKER"]
TOPIC = "subreddit"
START_DELAY = 30

CLIENT_ID = os.environ["CLIENT_ID"]
CLIENT_SECRET = os.environ["CLIENT_SECRET"]

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


def get_dict(comment):
    return {"id": comment.id, "author": comment.author.name,
            "timestamp": comment.created_utc, "parrent_id": comment.parent_id,
            "replies": len(comment.replies), "score": comment.score, 
            "permalink": comment.permalink, "body": comment.body}


def main():
    global producer
    print("Starting Reddit listener ...")
    producer = connect_to_kafka()
    time.sleep(START_DELAY)

    reddit = praw.Reddit(client_id=CLIENT_ID,
                         client_secret=CLIENT_SECRET,
                         user_agent='my user agent')

    subreddit = reddit.subreddit("+".join(SUBREDDITS))

    for comment in subreddit.stream.comments():
        comment_dict = get_dict(comment)
        print(comment.subreddit)
        producer.send(f"{TOPIC}-{comment.subreddit}", key=bytes(comment.id, "utf-8"),
                      value=bytes(json.dumps(comment_dict), "utf-8"))


if __name__ == "__main__":
    main()
