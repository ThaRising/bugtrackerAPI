import sqlite3


class Database:
    """
    Format Database Interface
    self.CONNECTION:
    """
    CONNECTION: sqlite3.connect = sqlite3.connect(":memory:")
    CURSOR = CONNECTION.cursor()

    def __init__(self):
        pass

    def __del__(self):
        """Format interface for destructor"""
        Database.CONNECTION.commit()
        Database.CONNECTION.close()

    @staticmethod
    def execute(query: str, params=None) -> None:
        """Formal interface for query execution"""
        with Database.CONNECTION:
            if params is None:
                Database.CURSOR.execute(query)
            elif type(params) == dict:
                Database.CURSOR.execute(query, params)

