from db import Database


class Schema:
    """
    Class to create schemas on the database before program gets started
    """
    def __init__(self):
        self.create_issueTable()
        self.create_userTable()

    @staticmethod
    def create_issueTable():
        """Creates he Issue Table if not yet created"""
        Database.execute("""
            CREATE TABLE IF NOT EXISTS Issue (
            id INTEGER PRIMARY KEY,
            Title TEXT,
            Desc TEXT,
            Tags TEXT,
            Assignee INTEGER DEFAULT 0,
            Status INTEGER DEFAULT 0,
            CreatedOn Date DEFAULT CURRENT_DATE,
            DueDate Date)""")

    @staticmethod
    def create_userTable():
        """Creates the User Table if not yet created"""
        Database.execute("""
            CREATE TABLE IF NOT EXISTS User (
            id INTEGER PRIMARY KEY,
            Name TEXT,
            CreatedOn Date DEFAULT CURRENT_DATE )""")


class UserTable:
    TABLENAME = "User"

    def __init__(self):
        pass

    @staticmethod
    def createUser(values: dict) -> None:
        """Creates a new User with a given set of values"""
        Database.execute("""
        INSERT INTO User VALUES 
        (:id, :Name, :CreatedOn)""", values)
