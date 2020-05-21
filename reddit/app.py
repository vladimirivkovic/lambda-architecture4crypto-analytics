#!/usr/bin/python3

import os
import time
import praw
from kafka import KafkaProducer
import kafka.errors

SUBREDDIT = os.environ["SUBREDDIT"]
KAFKA_BROKER = os.environ["KAFKA_BROKER"]
TOPIC = "subreddit-" + SUBREDDIT

CLIENT_ID = os.environ["CLIENT_ID"]
CLIENT_SECRET = os.environ["CLIENT_SECRET"]

reddit = praw.Reddit(client_id=CLIENT_ID,
                     client_secret=CLIENT_SECRET,
                     user_agent='my user agent')

subreddit = reddit.subreddit(SUBREDDIT)

while True:
    try:
        producer = KafkaProducer(bootstrap_servers=KAFKA_BROKER.split(","))
        print("Connected to Kafka!")
        break
    except kafka.errors.NoBrokersAvailable as e:
        print(e)
        time.sleep(3)

for comment in subreddit.stream.comments():
    producer.send(TOPIC, key=bytes(comment.author.name, 'utf-8'), value=bytes(comment.body, 'utf-8'))