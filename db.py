import sqlite3


class Database:
    def __init__(self, database: str):
        self.database = sqlite3.connect(database)
        self.connection = self.database.cursor()

    def __del__(self):
        self.database.commit()
        self.database.close()
