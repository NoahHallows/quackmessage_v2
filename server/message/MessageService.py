import psycopg2
from dotenv import load_dotenv, dotenv_values
import queue

import message_pb2
import message_pb2_grpc
from db_manager import db
from auth import jwt_auth

load_dotenv()

class MessageServicer(message_pb2_grpc.MessagerServicer):
    def __init__(self):
        self.active_clients = {}

    def sendMessage(self, request, context):
        print("Sending message")
        try:
            # Get username from auth token
            metadata = dict(context.invocation_metadata())
            auth_header = metadata.get('authorization', '')
            if auth_header.startswith('Bearer '):
                token = auth_header[len("Bearer "):]
                username = jwt_auth.get_username(token)
            else:
                return message_pb2.sendMessageResult(sendSuccessful=False, message_id=0)

            # Check sender and username match
            if username != request.sender:
                return message_pb2.sendMessageResult(sendSuccessful=False, message_id=0)

            conn = db.getConn()
            cursor = conn.cursor()
            cursor.execute("SELECT message_id FROM messages ORDER BY message_id DESC LIMIT 1")
            message_id = cursor.fetchone()
            print(message_id[0])
            message_id = message_id[0] + 1
            print(message_id)
            cursor.execute("INSERT INTO messages (sender, receiver, content, message_id, time_sent) VALUES (%s, %s, %s, %s, NOW())", (request.sender, request.receiver, request.content, message_id))
            # Check if receiver is online
            if request.receiver in self.active_clients:
                print("Receiver is active")
                message = {"sender": request.sender, "receiver": request.receiver, "content": request.content, "messageId": message_id}
                self.active_clients[request.receiver].put(message)
            conn.commit()
            cursor.close()
            print("Done")
            return message_pb2.sendMessageResult(sendSuccessful=True, message_id=message_id)
        except Exception as e:
            print(f"Error sending message: {e}")
            return message_pb2.sendMessageResult(sendSuccessful=False, message_id=0)

    def subscribeMessages(self, request, context):
        user_queue = queue.Queue()
        metadata = dict(context.invocation_metadata())
        auth_header = metadata.get('authorization', '')
        if auth_header.startswith('Bearer '):
            token = auth_header[len("Bearer "):]
            username = jwt_auth.get_username(token)
            self.active_clients[username] = user_queue
            print(self.active_clients)
            # Send old messages
            conn = db.getConn()
            cursor = conn.cursor()
            cursor.execute("SELECT sender, content, message_id, receiver FROM messages WHERE receiver = %s OR sender = %s", (username,username,))
            messages = cursor.fetchall()
            for message in messages:
                response = message_pb2.Message(sender=message[0], receiver=message[3], content=message[1], messageId=message[2])
                yield response
            try:
                while True:
                    new_message = user_queue.get()
                    print(new_message)
                    if new_message["receiver"] == username:
                        response = message_pb2.Message(sender=new_message["sender"],receiver=username,content=new_message["content"],messageId=new_message["messageId"])
                        yield response

            finally:
                del self.active_clients[username]

    def getContacts(self, request, context):
        metadata = dict(context.invocation_metadata())
        auth_header = metadata.get('authorization', '')
        if auth_header.startswith('Bearer '):
            token = auth_header[len("Bearer "):]
            username = jwt_auth.get_username(token)
            conn = db.getConn()
            cursor = conn.cursor()
            cursor.execute("SELECT username FROM users")
            users = cursor.fetchall()
            response = []
            for user in users:
                response.append(message_pb2.contact(name=user[0]))
            return message_pb2.contactList(contacts=response)



