import redis
import datetime

from flask import Flask,redirect, render_template, jsonify
from flask import request, url_for
app = Flask(__name__)

redis_host = 'localhost'
redis_port = 6379
redis_password = ""

r = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)
#r = redis.Redis(host='redis', port=6379)
@app.route('/')
def getIndex():
    #return redirect('/index.html')
    return render_template('/index.html') 

@app.route('/jsonee')
def getData():
    coins = int(r.hlen('wallet'))
    #hashes = r.get('hashes').decode("ascii")
    hashes = r.get('hashes')
    now = datetime.datetime.now()
    #print(f'now = {now}')
    now = now.strftime("%s")
    #print(f'now = {now}')
    now = int(now)/1000
    #print(f'now = {now}')
    #print(f'coins = {coins}')
   # print(f'hashes = {hashes}')
    return {
        "coins": coins,
        "hashes": hashes,
        "now": now,
        }

if __name__ == "__main__":
    app.run(host='0.0.0.0')

