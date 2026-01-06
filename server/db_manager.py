import psycopg2
import os
import sys
from time import sleep
import logging

class DatabaseManager:
    def __init__(self):
        DB_USER = os.environ.get("DB_USER")
        DB_PASSWORD = os.environ.get("DB_PASSWORD")
        if DB_USER is None or DB_PASSWORD is None:
            logging.error("Unable to get db username or password")
            sys.exit(1)
        for _ in range(0, 10):
            try:
                self.conn = psycopg2.connect(
                    user=DB_USER, password=DB_PASSWORD,
                    host='db', port='5432', database='quackmessage')
                fail = False
                break
            except:
                logging.warnign("Waiting for db server, sleeping for 2 seconds")
                fail = True
                sleep(2)

        if fail:
            logging.critical("Unable to connect to db")
            sys.exit(1)


    def getConn(self):
        return self.conn

db = DatabaseManager()
