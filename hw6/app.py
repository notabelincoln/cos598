 
import redis
import datetime

from flask import Flask, redirect, render_template, jsonify
from flask import request, url_for

app = Flask(__name__)


r = redis.Redis(host='redis', port=6379)

@app.route('/')
def getIndex():
    
    return render_template('/index.html') 

@app.route('/jsonee')
def getData():
    coins = int(r.hlen('wallet'))
    hashes = r.get('hashes').decode("ascii")
    now = datetime.datetime.now()
    now = now.strftime("%s")
    now = int(now)/1000
    return {
        "coins": coins,
        "hashes": hashes,
        "now": now,
        }

if __name__ == "__main__":
    app.run(host='0.0.0.0')

