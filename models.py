import db


class Schema:
    def __init__(self, database: db.Database):
        self.database = database
        self.create_issueTable()
        self.create_userTable()

    def create_issueTable(self):
        self.database.connection.execute("""
            CREATE TABLE IF NOT EXISTS Issue (
            id INTEGER PRIMARY KEY,
            Title TEXT,
            Desc TEXT,
            Tags TEXT,
            Assignee INTEGER DEFAULT 0,
            Status INTEGER DEFAULT 0,
            CreatedOn Date DEFAULT CURRENT_DATE,
            DueDate Date)""")

    def create_userTable(self):
        self.database.connection.execute("""
            CREATE TABLE IF NOT EXISTS User (
            id INTEGER PRIMARY KEY,
            Name TEXT,
            CreatedOn Date DEFAULT CURRENT_DATE )""")


# class IssueModel:
#     TABLENAME = "Issue"
#     def __init__(self, database: db.Database):
#         self.database = database
#
#     def
