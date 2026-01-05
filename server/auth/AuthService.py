# Authentication service

# Login: main function calls function here to hash password and then compare with db, returns true/false
# and generates jwt
# Signup: main function calls function here to hash password and store password, username ect in
# db. Returns true/false on user account creation success and returns jwt

from argon2 import PasswordHasher
import psycopg2
import jwt
from random import randint
import smtplib, ssl
import os
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv, dotenv_values
from sys import stdout
from datetime import datetime
from .jwt_auth import create_jwt
import logging
from threading import Lock
import grpc

# Import protobufs
import auth_pb2
import auth_pb2_grpc
from db_manager import db

VERSION = "0.0.0.1"

load_dotenv()

try:
    email_server = os.environ.get('EMAIL_SERVER')
    email_port = int(os.environ.get('EMAIL_PORT'))
    email_username = os.environ.get('EMAIL_USERNAME')
    email_password = os.environ.get('EMAIL_PASSWORD')
    if email_server is None or email_port is None or email_password is None or email_username is None:
        raise NameError
except NameError:
    logging.warning("Cannot get email settings from environment")

if email_server is None:
    logging.warning("Unable to access email_server environment var")

if email_port is None:
    logging.warning("Unable to access email_port environment var")

if email_username is None:
    logging.warning("Unable to access email_username environment var")

if email_password is None:
    logging.warning("Unable to access email_password environment var")

# Convert the list of bytes to a single variable
def db_binary_to_binary(db_binary):
    binary = b''
    for collumn in db_binary:
        for section in collumn:
            for byte in section:
                binary = binary + byte

    return binary


class AuthServicer(auth_pb2_grpc.QuackMessageAuthServicer):

    def __init__(self):
        self.email_verification_dict = {}
        self.verified_emails = []
        self.email_lock = Lock()

    # Login function
    def Login(self, request, context):
        logging.info(f"Login for user {request.username}")
        if (len(request.username) > 256):
            # Username is too long
            logging.warning(f"Username {request.username} is too long")
            return auth_pb2.LoginResult(success=False, auth_token="")
        try:
            conn = db.getConn()
            cursor = conn.cursor()
            cursor.execute("SELECT password_hash FROM users WHERE username = %s", (request.username,))
            password_hash = db_binary_to_binary(cursor.fetchall())

        except Exception as e:
            logging.warning(f"Password not found: {e}")

        try:
            ph = PasswordHasher()
            ph.verify(password_hash, request.password)
            logging.info("Passwords match")
            cursor.execute("UPDATE users SET last_login = %s WHERE username = %s", (datetime.now(timezone.utc), request.username,))
            conn.commit()
            cursor.close()

            token = create_jwt(request.username)
            logging.info(f"User {request.username} has successfully logged in")
            return auth_pb2.LoginResult(success=True, auth_token=token)

        except Exception as e:
            logging.info(f"Passwords do not match for user {request.username}: {e}")
            conn.commit()
            cursor.close()

            return auth_pb2.LoginResult(success=False, auth_token="")
        context.abort(grpc.StatusCode.UNAUTHENTICATED, "Error")

    def VerifyEmail(self, request, context):
        # Check email isn't already registered
        if len(request.email) > 254:
            return auth_pb2.VerificationEmailSent(emailSent=False)
        conn = db.getConn()
        cur = conn.cursor()
        logging.info("Connected to db")
        cur.execute("SELECT 1 FROM users WHERE email = %s;", (request.email,))
        if cur.fetchone() is not None:
            return auth_pb2.VerificationEmailSent(emailSent=False)
            logging.info("Email is already in db")

        email_context = ssl.create_default_context()
        with smtplib.SMTP_SSL(email_server, email_port, context=email_context) as server:
            server.login(email_username, email_password)
            logging.info("Logged in to email server")
            email_verification_code = randint(100000, 999999)
            with self.email_lock:
                self.email_verification_dict[request.email] = email_verification_code

            message = MIMEMultipart("alternative")
            message["Subject"] = "Quackmessage verification code"
            message["From"] = email_username
            message["To"] = request.email

            message_text = "Hello,\nYour verification code is: {code}\nRegards Quackmessage automated email bot"
            part1 = MIMEText(message_text.format(code=email_verification_code), "plain")
            message.attach(part1)
            server.sendmail(email_username, request.email, message.as_string())
            logging.debug("Email sent")
            return auth_pb2.VerificationEmailSent(emailSent=True)

    def CheckCode(self, request, context):
        with self.email_lock:
            if request.code == self.email_verification_dict[request.email]:
                self.verified_emails.append(request.email)
                self.email_verification_dict.pop(request.email)
                return auth_pb2.VerificationCodeMatches(verified=True)
            else:
                self.email_verification_dict.pop(request.email)
                return auth_pb2.VerificationCodeMatches(verified=False)

    def CreateUser(self, request, context):
        if len(request.email) > 254:
            # Email is too long
            return auth_pb2.CreateUserResult(success=False, auth_token="")
        if len(request.username) > 256:
            return auth_pb2.CreateUserResult(success=False, auth_token="")
        conn = db.getConn()
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM users WHERE username = %s;", (request.username,))
        if cur.fetchone() is None:
            if (request.email in self.verified_emails):
                self.verified_emails.remove(request.email)
                ph = PasswordHasher()
                password_hash = ph.hash(request.password)
                try:
                    cur.execute("INSERT INTO users (email, username, password_hash, account_creation_date, messages_sent, messages_received) VALUES (%s, %s, %s, %s, %s, %s)", (request.email, request.username, password_hash, datetime.now(timezone.utc), 0, 0))
                    conn.commit()
                    cur.close()

                    logging.info("Successfully created account")
                    token = create_jwt(request.username)
                    return auth_pb2.CreateUserResult(success=True, auth_token=token)
                except Exception as e:
                    logging.warning(f"Error inserting user into database: {e}")
        else:
            logging.info("User exists or email is unverified")

        conn.commit()
        cur.close()


        return auth_pb2.CreateUserResult(success=False, auth_token="")

    def CheckVersion(self, request, context):
        if (request.version == VERSION):
            return auth_pb2.ValidVersion(valid=True, valid_version_num=VERSION)
        else:
            return auth_pb2.ValidVersion(valid=False, valid_version_num=VERSION)

