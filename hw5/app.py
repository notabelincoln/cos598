import datetime
import sqlite3 as lite

from flask import Flask, redirect, render_template, jsonify
from flask import request, url_for

app = Flask(__name__)


######################################################################
DATABASE = '/tmp/dockercoins.db'
con = lite.connect(DATABASE)
c = con.cursor()
c.execute('CREATE TABLE IF NOT EXISTS coins (attemptid INTEGER PRIMARY KEY AUTOINCREMENT, hash TEXT, attempts INTEGER);')
######################################################################
@app.route('/')
def getIndex():    
    return render_template('/index.html') 

@app.route('/jsonee')
def getData():
    coins2 = 0
    hashes2 = 0
    con = lite.connect(DATABASE)
    w = con.cursor()
    ################
    w.execute('SELECT * FROM coins;')
    data = w.fetchall()
    coins2 = len(data)
    hashes2 = data[2][2]
    ################
    now = datetime.datetime.now()
    now = now.strftime("%s")
    now = int(now)/1000
    return {
        "coins": coins2,
        "hashes": hashes2,
        "now": now,
        }

if __name__ == "__main__":
    app.run(host='0.0.0.0')

