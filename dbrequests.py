import sqlite3

class GameDB:

    def __init__(self):
        self.connection = None
        self.cursor = None

    def establish_connection(self, db_file):
        try:
            self.connection = sqlite3.connect(db_file)
            self.cursor = self.connection.cursor()
            return True
        except ValueError:
            return False

    def close_connection(self):
        try:
            self.connection.close()
            return True
        except ValueError:
            return False
