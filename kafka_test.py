#!/usr/bin/python3

from kafka import KafkaProducer
import json
from twitter import TwitterStream, OAuth
import datetime
import time
import threading
import os
from pathlib import Path
from api.create_topic import create_topic
from api.connection_helper import ConnectionHelper


home = str(Path.home())

with open("/{0}/twitter_keys.txt".format(home), "r") as f:
    ck = f.readline().strip()
    cs = f.readline().strip()
    ak = f.readline().strip()
    a_s = f.readline().strip()
    config = {
        "consumer_key" : ck,
        "consumer_secret" : cs,
        "access_key" : ak,
        "access_secret" : a_s
    }


if __name__ == '__main__':
    search_term = "trump"  # twitter
    topic = 'trump'        # kafka
    topic_id = create_topic(topic, ConnectionHelper())
    producer = KafkaProducer()

    while True:
        try:
            count = 0
            st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H:%M:%S')
            auth = OAuth(
                config["access_key"],
                config["access_secret"],
                config["consumer_key"],
                config["consumer_secret"]
            )
            stream = TwitterStream(auth = auth, secure = True)
            tweet_iter = stream.statuses.filter(track = search_term)
            for tweet in tweet_iter:
                future = producer.send(topic, str.encode(tweet["text"]))
                result = future.get(timeout=60)
                time.sleep(0.2)
        except Exception as e:
            print(e)
            time.sleep(60)
