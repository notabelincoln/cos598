import redis
import logging
import os
from redis import Redis
import requests
import time
import random

DEBUG = os.environ.get("DEBUG", "").lower().startswith("y")

log = logging.getLogger(__name__)
if DEBUG:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)
    logging.getLogger("requests").setLevel(logging.WARNING)


redis = Redis("redis")


def distract_worker():
    r = requests.get("http://worker/")
    return r.text

if __name__ == "__main__":
    while True:
        try:
            distract_worker()
            sleep_interval = random.uniform(0.1, 0.5)
            time.sleep(sleep_interval)
        except:
            log.exception("In coworker loop")
            log.error("Waiting 10s and restarting.")
            time.sleep(10)


