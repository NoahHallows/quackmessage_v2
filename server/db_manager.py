import psycopg2

class DatabaseManager:
    def __init__(self):
        self.conn = psycopg2.connect(
            user='quackmessage_db_user', password='m4S0cFOrFIRBdip1h3jFl0DNn',
            host='192.168.1.150', port='5432', database='quackmessage')

    def getConn(self):
        return self.conn

db = DatabaseManager()
