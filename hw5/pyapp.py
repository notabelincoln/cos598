import redis
import datetime
import sqlite3 as lite



from flask import Flask,redirect, render_template, jsonify
app = Flask(__name__)

redis_host = 'localhost'
redis_port = 6379
redis_password = ""

DATABASE = 'dockercoins.db'
con = None
upd = None

con = lite.connect('dockercoins.db')
c = con.cursor()

try:
    c.execute('DROP TABLE IF EXISTS coins')
except:
    c.execute('CREATE TABLE coins (hashes INTEGER PRIMARY KEY AUTOINCREMENT, coins INTEGER)')


r = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)
#r = redis.Redis(host='redis', port=6379)
@app.route('/')
def getIndex():
    #return redirect('/index.html')
    return render_template('/index.html') 

@app.route('/jsonee')
def getData():

    c.execute('SELECT hashes FROM coins')
    hashes2 = c.fetchall()
    coins2 = len(hashes)

    coins = int(r.hlen('wallet'))
    #hashes = r.get('hashes').decode("ascii")
    hashes = r.get('hashes')

    now = datetime.datetime.now()
    print(f'now = {now}')
    now = now.strftime("%s")
    print(f'now = {now}')
    now = int(now)/1000
    print(f'now = {now}')
    print(f'coins = {coins2}')
    print(f'hashes = {hashes2}')
    return {
        "coins": coins2,
        "hashes": hashes2,
        "now": now,
        }

if __name__ == "__main__":
    app.run(host='0.0.0.0')

