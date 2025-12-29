import psycopg2
import os
import sys
from time import sleep

class DatabaseManager:
    def __init__(self):
        DB_USER = os.environ.get("DB_USER")
        DB_PASSWORD = os.environ.get("DB_PASSWORD")
        if DB_USER is None or DB_PASSWORD is None:
            print("Unable to get db username or password", file=sys.stderr)
            sys.exit(1)
        for x in range(0, 5):
            try:
                self.conn = psycopg2.connect(
                    user=DB_USER, password=DB_PASSWORD,
                    host='db', port='5432', database='quackmessage')
                break
            except:
                print("Waiting for db server, sleeping for 2 seconds")
                sleep(2)


    def getConn(self):
        return self.conn

db = DatabaseManager()
