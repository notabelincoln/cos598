import datetime

from flask import Flask, redirect, render_template, jsonify
from flask import request, url_for

app = Flask(__name__)

@app.route('/')
def getIndex():
    
    return render_template('/index.html') 

@app.route('/jsonee')
def getData():
    coins_get = requests.get("http://worker/coins")
    hashes_get = requests.get("http://worker/hashes")
    coins = int(coins_get.text)
    hashes = int(hashes_get.text)
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

