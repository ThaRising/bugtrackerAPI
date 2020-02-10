from flask import Flask
from models import Schema, UserTable
from db import Database
import sqlite3

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"


if __name__ == "__main__":
    Schema()
    UserTable.createUser({"id": "3", "Name": "Bon", "CreatedOn": "12345"})
    print(Database.CURSOR.execute("SELECT * FROM User").fetchall())
    app.run(debug=True)
