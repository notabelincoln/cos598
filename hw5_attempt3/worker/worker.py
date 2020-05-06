import redis
import logging
import os
from redis import Redis
import requests
import time
import threading
import random
import sqlite3 as lite

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


con = lite.connect('/db/dockercoins.db')
c = con.cursor()
c.execute('CREATE TABLE IF NOT EXISTS coins (hash TEXT, attempts INTEGER)')



time_to_work = False
loops_done2 = 0

def get_random_bytes():
    r = requests.get("http://rng/32")
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
                     .format(loops_done2))
            #####################
            c.execute('SELECT hash FROM coins;')
            num_hashes = c.fetchall()

            c.execute('REPLACE INTO coins (id, attempts) VALUES (?, ?);', (len(num_hashes), loops_done2))
            con.commit()
            #####################
            loops_done = 0
            deadline = time.time() + interval
        work_once()
        loops_done += 1
        loops_done2 += 1


def work_once():
    existing_hash = 0
    log.debug("Doing one unit of work")
    time.sleep(0.1)
    random_bytes = get_random_bytes()
    hex_hash = hash_bytes(random_bytes)
    if not hex_hash.startswith('0'):
        log.debug("No coin found")
        return
    log.info("Coin found: {}...".format(hex_hash[:8]))
    ######################
    c.execute('SELECT hash FROM coins;')
    hashes = c.fetchall()
    for x in range(len(hashes)):
        if hashes[x][0] == hex_hash:
            existing_hash = 1
            break
    if existing_hash == 0:
        c.execute('INSERT INTO coins (hash, attempts) VALUES (?, ?);', (hex_hash[], loops_done2))
        con.commit()
    ######################
    if existing_hash == 1:
        log.info("We already had that coin")

def work_thread():
    def run():
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

@app.before_first_request(work_thread())

@app.route('/coins/')
def sendCoins():
    c.execute('SELECT hash FROM coins')
    return_coins = c.fetchall()
    return len(return_coins)

@app.route('/hashes/')
def sendCoins():
    c.execute('SELECT attempts FROM coins')
    arr_coins = c.fetchall()
    return_hashes = arr_coins[len(arr_coins) - 1][0]
    return len(return_hashes)

if __name__ == "__main__":
    app.run(host='0.0.0.0', threaded=True, port=80)
