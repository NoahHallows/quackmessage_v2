import psycopg2
from dotenv import load_dotenv, dotenv_values
import queue
import logging
import time
from threading import Lock
from sys import stdout

import message_pb2
import message_pb2_grpc
from db_manager import db
from auth import jwt_auth

load_dotenv()

logging.basicConfig(
    format="{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
    level=logging.DEBUG,
    handlers=[
        logging.StreamHandler(stdout)
    ]
)

def current_milli_time():
    return round(time.time() * 1000)

class MessageServicer(message_pb2_grpc.MessagerServicer):
    def __init__(self):
        self.client_lock = Lock()
        self.send_message_lock = Lock()
        self.active_clients = {}

    def sendMessage(self, request, context):
        logging.info("Sending message")
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
            # To prevent two messages having the same message_id
            with self.send_message_lock:
                try:
                    cursor.execute("SELECT message_id FROM messages ORDER BY message_id DESC LIMIT 1")
                    message_id = cursor.fetchone()
                    logging.debug(message_id[0])
                    message_id = message_id[0] + 1
                    logging.debug(message_id)

                except:
                    logging.warning("It appears there are no messages in db")
                    message_id = 1
                cursor.execute("INSERT INTO messages (sender, receiver, content, message_id, time_sent) VALUES (%s, %s, %s, %s, NOW())", (request.sender, request.receiver, request.content, message_id))
                cursor.execute("UPDATE users SET messages_sent = messages_sent + 1 WHERE username = %s", (request.sender,))
                cursor.execute("UPDATE users SET messages_received = messages_received + 1 WHERE username = %s", (request.receiver,))
                conn.commit()
                cursor.close()

            # Check if receiver is online
            if request.receiver in self.active_clients:
                logging.debug("Receiver is active")
                message = {"sender": request.sender, "receiver": request.receiver, "content": request.content, "messageId": message_id, "timeStamp": current_milli_time()}
                with self.send_message_lock:
                    self.active_clients[request.receiver].put(message)
            logging.info("Done sending message")
            return message_pb2.sendMessageResult(sendSuccessful=True, message_id=message_id)
        except Exception as e:
            logging.error(f"Error sending message: {e}")
            return message_pb2.sendMessageResult(sendSuccessful=False, message_id=0)

    def subscribeMessages(self, request, context):
        user_queue = queue.Queue()
        metadata = dict(context.invocation_metadata())
        auth_header = metadata.get('authorization', '')
        if auth_header.startswith('Bearer '):
            token = auth_header[len("Bearer "):]
            username = jwt_auth.get_username(token)
            with self.send_message_lock:
                self.active_clients[username] = user_queue
            # Send old messages
            conn = db.getConn()
            cursor = conn.cursor()
            cursor.execute("SELECT sender, content, message_id, time_sent, receiver FROM messages WHERE receiver = %s OR sender = %s", (username,username,))
            messages = cursor.fetchall()
            logging.info(f"Sending {len(messages)} to client {username}")
            for message in messages:
                response = message_pb2.Message(sender=message[0], receiver=message[4],
                                               content=message[1], messageId=message[2],
                                               sent_at=message[3])
                yield response
            try:
                while True:
                    with self.send_message_lock:
                        new_message = user_queue.get()
                    if new_message["receiver"] == username:
                        response = message_pb2.Message(sender=new_message["sender"],receiver=username,content=new_message["content"],messageId=new_message["messageId"], sent_at=new_message["timeStamp"])
                        yield response

            finally:
                with self.send_message_lock:
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



