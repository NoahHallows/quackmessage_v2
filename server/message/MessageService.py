import psycopg2
from dotenv import load_dotenv, dotenv_values

import message_pb2
import message_pb2_grpc
from db_manager import db

load_dotenv()

class MessageServicer(message_pb2_grpc.MessagerServicer):
    def __init__(self):
        pass

    def sendMessage(self, request, context):
        print("Sending message")
        try:
            conn = db.getConn()
            cursor = conn.cursor()
            cursor.execute("SELECT message_id FROM messages ORDER BY message_id DESC LIMIT 1")
            message_id = cursor.fetchone() + 1
            cursor.execute("INSERT INTO messages (sender, receiver, content, message_id, time_sent) VALUES (%s, %s, %s, %s, NOW())", request.sender, request.receiver, request.content, message_id)
            conn.commit()
            cursor.close()
            print("Done")
            return message_pb2.SendMessageResult(success=True, message_id=message_id)
        except Exception as e:
            print("Error sending message: {e}")
            return message_pb2.SendMessageResult(success=False, message_id=0)
