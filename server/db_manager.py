import psycopg2

class DatabaseManager:
    def __init__(self):
        self.pool = psycopg2.pool.SimpleConnectionPool(
            2, 10, user='quackmessage_db_user', password='m4S0cFOrFIRBdip1h3jFl0DNn',
            host='192.168.1.150', port='5432', database='quackmessage')

    def getConn(self):
        return self.pool.getconn()

    def putConn(self, conn):
        self.pool.putconn(conn)

db = DatabaseManager()
