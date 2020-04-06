from flask import Flask, render_template, request
import sqlite3 as lite

app = Flask(__name__)
DATABASE = '/tmp/jordan.db'

con = lite.connect("jordan.db")
c = con.cursor()
c.execute('CREATE TABLE IF NOT EXISTS cars (id INTEGER PRIMARY KEY AUTOINCREMENT, license TEXT, make TEXT, model TEXT, color TEXT)')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/newcar/')
def newcar():
    return render_template('newcar.html')

@app.route('/addcar/', methods = ['POST', 'GET'])
def addcar():
    if request.method == 'POST':
        try:
            crlp = request.form['crlp']
            crmk = request.form['crmk']
            crmdl = request.form['crmdl']
            crclr = request.form['crclr']

            with lite.connect("jordan.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO cars (license, make, model, color) VALUES (?,?,?,?)", (crlp, crmk, crmdl, crclr))
                con.commit()
                msg = "Record successfully added"
    
        except:
            con.rollback()
            msg = "Error in insert operation"
    
        finally:
            return render_template("result.html", msg = msg)
            con.close()

@app.route('/list/')
def list():
    con = lite.connect("jordan.db")
    con.row_factory = lite.Row
    
    cur = con.cursor()
    cur.execute("SELECT * FROM cars")
    rows = cur.fetchall();
    return render_template("list.html", rows = rows)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
