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
from sys import stderr
from datetime import datetime
from .jwt_auth import create_jwt

# Import protobufs
import auth_pb2
import auth_pb2_grpc
from db_manager import db

load_dotenv()

try:
    email_server = os.environ.get('EMAIL_SERVER')
    email_port = int(os.environ.get('EMAIL_PORT'))
    email_username = os.environ.get('EMAIL_USERNAME')
    email_password = os.environ.get('EMAIL_PASSWORD')
    if email_server is None or email_port is None or email_password is None or email_username is None:
        raise NameError
except NameError:
    print("Cannot get email settings from environment", file=stderr)

if email_server is None:
    print("Unable to access email_server environment var", file=stderr)
    sys.exit(1)
if email_port is None:
    print("Unable to access email_port environment var", file=stderr)
    sys.exit(1)
if email_username is None:
    print("Unable to access email_username environment var", file=stderr)
    sys.exit(1)
if email_password is None:
    print("Unable to access email_password environment var", file=stderr)
    sys.exit(1)

print(f"server: {email_server}, port: {email_port}, username: {email_username}, password: {email_password}")
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
        self.email = None
        self.email_verified = False
        self.email_verification_code = None


    # Login function
    def Login(self, request, context):
        print(f"Login for user {request.username} at {datetime.now()}")
        try:
            conn = db.getConn()
            cursor = conn.cursor()
            cursor.execute("SELECT password_hash FROM users WHERE username = %s", (request.username,))
            password_hash = db_binary_to_binary(cursor.fetchall())

        except Exception as e:
            print(f"Password not found: {e}", file=stderr)

        try:
            ph = PasswordHasher()
            ph.verify(password_hash, request.password)
            print("Passwords match")
            cursor.execute("UPDATE users SET last_login = NOW() WHERE username = %s", (request.username,))
            conn.commit()
            cursor.close()

            token = create_jwt(request.username)
            return auth_pb2.LoginResult(success=True, auth_token=token)

        except Exception as e:
            print(f"Passwords do not match: {e}")
            conn.commit()
            cursor.close()

            return auth_pb2.LoginResult(success=False, auth_token="")
        context.abort(grpc.StatusCode.UNAUTHENTICATED, "Error")

    def VerifyEmail(self, request, context):
        # Create a secure SSL context
        context = ssl.create_default_context()

        # Check email isn't already registered
        conn = db.getConn()
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM users WHERE email = %s;", (request.email,))
        if cur.fetchone() is not None:
            return auth_pb2.VerificationEmailSent(emailSent=False)

        with smtplib.SMTP_SSL(email_server, email_port, context=context) as server:
            server.login(email_username, email_password)
            self.email_verification_code = randint(100000, 999999)
            message = MIMEMultipart("alternative")
            message["Subject"] = "Quackmessage verification code"
            message["From"] = email_username
            message["To"] = request.email

            message_text = "Hello,\nYour verification code is: {code}\nRegards Quackmessage automated email bot"
            part1 = MIMEText(message_text.format(code=self.email_verification_code), "plain")
            message.attach(part1)
            server.sendmail(email_username, request.email, message.as_string())
            self.email = request.email
            return auth_pb2.VerificationEmailSent(emailSent=True)

    def CheckCode(self, request, context):
        if request.code == self.email_verification_code:
            self.email_verified = True
            return auth_pb2.VerificationCodeMatches(verified=True)
        else:
            self.email_verified = False
            return auth_pb2.VerificationCodeMatches(verified=False)

    def CreateUser(self, request, context):
        conn = db.getConn()
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM users WHERE username = %s;", (request.username,))
        if cur.fetchone() is None and self.email is not None and self.email_verified == True:
            ph = PasswordHasher()
            password_hash = ph.hash(request.password)
            try:
                cur.execute("INSERT INTO users (email, username, password_hash, account_creation_date, messages_sent, messages_received) VALUES (%s, %s, %s, NOW(), %s, %s)", (self.email, request.username, password_hash, 0, 0))
                conn.commit()
                cur.close()

                print("Done")
                token = create_jwt(request.username)
                return auth_pb2.CreateUserResult(success=True, auth_token=token)
            except Exception as e:
                print(f"Error inserting user into database: {e}", file=stderr)
        else:
            print("User exists or email is unverified", file=stderr)

        conn.commit()
        cur.close()


        return auth_pb2.CreateUserResult(success=False, auth_token="")

