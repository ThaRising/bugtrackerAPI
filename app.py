from flask import Flask
from models import Schema
import db
import sqlite3

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"


if __name__ == "__main__":
    data = sqlite3.connect(":memory:")
    database = data.cursor()
    database.execute("""
        CREATE TABLE IF NOT EXISTS User (
        id INTEGER PRIMARY KEY,
        Name TEXT,
        CreatedOn Date DEFAULT CURRENT_DATE )""")
    database.execute("""INSERT INTO User VALUES ('7', 'Ben', '2')""")
    database.execute("""SELECT * FROM User WHERE Name='Ben'""")
    print(database.fetchall())
    app.run(debug=True)
