import psycopg2
import os
import sys

class DatabaseManager:
    def __init__(self):
        DB_USER = os.environ.get("DB_USER")
        DB_PASSWORD = os.environ.get("DB_PASSWORD")
        if DB_USER is None or DB_PASSWORD is None:
            print("Unable to get db username or password", file=sys.stderr)
            sys.exit(1)
        self.conn = psycopg2.connect(
            user=DB_USER, password=DB_PASSWORD,
            host='192.168.1.150', port='5432', database='quackmessage')

    def getConn(self):
        return self.conn

db = DatabaseManager()
