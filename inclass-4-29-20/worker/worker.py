import redis
import logging
import os
from redis import Redis
import requests
import time
import threading

from flask import Flask, redirect, render_template, jsonify
from flask import request, url_for

app = Flask(__name__)

DEBUG = os.environ.get("DEBUG", "").lower().startswith("y")

log = logging.getLogger(__name__)
if DEBUG:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)
    logging.getLogger("requests").setLevel(logging.WARNING)


redis = Redis("redis")

@app.before_first_request
def work_thread():
    def run():
        while(1):
            log.error("buya!!")
            try:
                log.error("Waiting.......")
                work_loop()
            except:
                log.exception("In work loop:")
                log.error("Waiting 10s and restarting.")
                time.sleep(10)

    thread = threading.Thread(target=run)
    thread.start()


def get_random_bytes():
    r = requests.get("http://rng/32")
    return r.content

def distracted_by_coworker():
    r = requests.get("http://coworker/harass")
    return r.content


def hash_bytes(data):
    r = requests.post("http://hasher/",
                      data=data,
                      headers={"Content-Type": "application/octet-stream"})
    hex_hash = r.text
    return hex_hash


def work_loop(interval=1):
    deadline = 0
    loops_done = 0
    while True:
        if time.time() > deadline:
            log.info("{} units of work done, updating hash counter"
                     .format(loops_done))
            redis.incrby("hashes", loops_done)
            loops_done = 0
            deadline = time.time() + interval
        work_once()
        loops_done += 1


def work_once():
    time_to_work = 0
    log.debug("Doing one unit of work")
    time.sleep(0.1)
    time_to_work = distracted_by_coworker()
    if time_to_work > 127:
        time.sleep(10)
    random_bytes = get_random_bytes()
    hex_hash = hash_bytes(random_bytes)
    if not hex_hash.startswith('0'):
        log.debug("No coin found")
        return
    log.info("Coin found: {}...".format(hex_hash[:8]))
    created = redis.hset("wallet", hex_hash, random_bytes)
    if not created:
        log.info("We already had that coin")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, threaded=True)


