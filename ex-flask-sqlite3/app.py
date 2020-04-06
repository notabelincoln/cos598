from flask import Flask, render_template
import sqlite3 as lite

app = Flask(__name__)
DATABASE = '/tmp/jordan.db'

@app.route('/')
def hello():
	con = None
	upd = None

	con = lite.connect(DATABASE)
	c = con.cursor()
	try:
		c.execute('CREATE TABLE cars (carid INTEGER PRIMARY KEY AUTOINCREMENT, model STRING, color STRING, cost STRING)')
	except:
		pass
	finally:
		c.execute('SELECT * FROM cars')
		count = c.fetchone()
		if count == None:
			c.execute('INSERT INTO cars(carid, model, color, cost) VALUES("1", "CRV", "Red", "3300")')
			upd = 1
		elif count[0] == None:
			pass
		else:
			upd = int(count[0]) + 1
			c.execute('INSERT INTO cars(carid, model, color, cost) VALUES("2", "SENTRA", "BLUE", "1000")')
			con.commit()
			c.close()

			if con:
				con.close()

	rows = c.fetchall()
	return render_template('list.html', rows = rows)

if __name__ == "__main__":
	app.run(host="0.0.0.0", debug=True)
