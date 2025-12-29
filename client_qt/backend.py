from PySide6.QtCore import QObject, Slot, Property, Signal
import auth_pb2
import auth_pb2_grpc
import message_pb2
import message_pb2_grpc
import _credentials
import grpc
import threading
from datetime import datetime
import jwt
import sys
import logging

ISSUER = "Quackmessage"
AUDIENCE = "Quackmessage_app"

logging.basicConfig(
    format="{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
    level=logging.DEBUG,
)




class Backend(QObject):
    logging.info("Starting")
    # Lock for updating class wide variables
    _var_lock = threading.Lock()
    _stub_lock = threading.Lock()
    # Signals
    loginSuccess = Signal()
    newMessage = Signal(str, str, int, float)
    loginFail = Signal()
    sendEmailFail = Signal()
    emailVerificationFail = Signal()
    accountCreationFail = Signal()
    addContactSignal = Signal(str)
    setUserName = Signal(str)
    requestFinished = Signal()
    active_contact = ""
    master_message_list = []
    # Auth stuff
    def __init__(self):
        super().__init__()
        try:
            with self._var_lock:
                self.HOST = "message.quackmail.com.au:5555"
                self._user_email = ""
                self.username = ""
                self.token = ""
            self._update_channel("")
            logging.info("Successfully connected to server and intialised")
        except Exception as e:
            logging.critical(f"Unable to connect to server, exiting!\n{e}")
            # TODO Exit

    def _update_channel(self, token):
        logging.info("Updating channel")
        try:
            with self._stub_lock:
                call_credentials = grpc.access_token_call_credentials(token)
                channel_credentials = grpc.ssl_channel_credentials(_credentials.TLS_PUB)
                composite_credentials = grpc.composite_channel_credentials(channel_credentials, call_credentials)
                channel = grpc.secure_channel(self.HOST, composite_credentials)
                authStub = auth_pb2_grpc.QuackMessageAuthStub(channel)
                messageStub = message_pb2_grpc.MessagerStub(channel)

                # Check if theres an old channel
                if hasattr(self, 'channel'):
                    self.channel.close()

                self.authStub = authStub
                self.channel = channel
                self.messageStub = messageStub
        except Exception as e:
            logging.error(f"Error creating channel: {e}")

    # This allows QML to call a Python function
    @Slot(str, str)
    def login(self, username, password):
        logging.info("Login function called, starting helper thread")
        # Start login helper function so we don't block the main ui thread
        threading.Thread(target=self._login_helper, args=(username, password), daemon=True).start()

    # We're back to helper functions again
    def _login_helper(self, username, password):
        logging.info(f"Attempting login for: {username}")
        try:
            request = auth_pb2.LoginMessage(username=username, password=password)
            login_future = self.authStub.Login.future(request)
            result = login_future.result()
            if result.success == True:
                with self._var_lock:
                    self.username = username
                    self.token = result.auth_token
                # Verify jwt was signed by valid key
                try:
                    jwt.decode(result.auth_token, _credentials.JWT_PUB,
                               algorithms=["RS256"], audience=AUDIENCE, issuer=ISSUER)
                except Exception as e:
                    logging.error(f"ERROR VALIDATING AUTH TOKEN!! Exiting\n{e}")
                # Create new channel with auth token in metadata
                # This is fine because it is done before there are any
                self._update_channel(result.auth_token)
                self.loginSuccess.emit()
                # Start receive message stream
                self.receiveMessageThread = threading.Thread(target=self.receiveMessage, args=(), daemon=True)
                self.receiveMessageThread.start()
                getContactsThread = threading.Thread(target=self.getContacts, args=(),daemon=True)
                getContactsThread.start()
                self.setUserName.emit(self.username)
            else:
                logging.warning(f"Error logging in for user {username}")
                self.loginFail.emit()
        except Exception as e:
            logging.error(f"Network error while logging in: {e}")
            self.loginFail.emit()
        finally:
            self.requestFinished.emit()


    # This allows Python to send data back to QML
    @Slot(str)
    def request_email_code(self, email):
        logging.info("Email verification code requested")
        threading.Thread(target=self._request_email_helper, args=(email,), daemon=True).start()

    def _request_email_helper(self, email):
        logging.debug(f"Sending code to: {email}")
        try:
            request = auth_pb2.VerifyEmailMessage(email=email)
            email_code = self.authStub.VerifyEmail.future(request)
            result = email_code.result()
            logging.debug(f"Email sent: {result.emailSent}")
            if result.emailSent == False:
                logging.warning("Error sending email")
                self.sendEmailFail.emit()
        except Exception as e:
            logging.error(f"Error sending email: {e}")
            self.sendEmailFail.emit()
        finally:
            self.requestFinished.emit()



    @Slot(int)
    def verify_email_code(self, code):
        logging.info("Verify email code function has been called")
        threading.Thread(target=self._verify_email_helper, args=(code,), daemon=True).start()

    def _verify_email_helper(self, code):
        logging.debug(f"Verification code {code}")
        try:
            request = auth_pb2.VerificationCodeMessage(code=code)
            verify_result = self.authStub.CheckCode.future(request)
            result = verify_result.result()
            if result.verified == False:
                logging.info("Verification has failed, likely wrong code was entered")
                self.emailVerificationFail.emit()
        except Exception as e:
            logging.error(f"Error verifying code: {e}")
            self.emailVerificationFail.emit()
        finally:
            self.requestFinished.emit()

    @Slot(str, str)
    def create_account(self, username, password):
        logging.info("Creating user")
        threading.Thread(target=self._create_account_helper, args=(username, password), daemon=True).start()

    def _create_account_helper(self, username, password):
        logging.debug(f"Create account helper: {username}, {password}")
        try:
            request = auth_pb2.CreateUserMessage(username=username, password=password)
            create_account_result = self.authStub.CreateUser.future(request)
            result = create_account_result.result()
            if result.success == True:
                logging.info("Create user succeeded, putting auth token in channel and starting message thread")
                with self._var_lock:
                    self.token = result.auth_token
                    self.username = username
                # Verify jwt was signed by valid key
                try:
                    jwt.decode(result.auth_token, _credentials.JWT_PUB,
                               algorithms=["RS256"], audience=AUDIENCE, issuer=ISSUER)
                except Exception as e:
                    logging.error(f"ERROR VALIDATING AUTH TOKEN!! Exiting\n{e}")
                    # TODO something here
                # Create new channel with auth token in metadata
                self._update_channel(result.auth_token)
                self.loginSuccess.emit()
                # Start receive message stream
                self.receiveMessageThread = threading.Thread(target=self.receiveMessage, args=(), daemon=True)
                self.receiveMessageThread.start()
                getContactsThread = threading.Thread(target=self.getContacts, args=(),daemon=True)
                getContactsThread.start()
                self.setUserName.emit(self.username)
            else:
                logging.warning("Unable to create account")
                self.accountCreationFail.emit()

        except Exception as e:
            logging.error(f"Error creating user {e}")
            self.accountCreationFail.emit()
        finally:
            self.requestFinished.emit()
    # Message stuff
    @Slot(str)
    def send_message(self, message):
        logging.debug(f"Sending {message} to {self.active_contact}")
        try:
            request = message_pb2.Message(sender=self.username, receiver=self.active_contact, content=message)
            send_message_result = self.messageStub.sendMessage.future(request)
            result = send_message_result.result()
            logging.debug(f"Success: {result.sendSuccessful}, message id: {result.message_id}")
            if result.sendSuccessful == True:
                time_sent = datetime.now().timestamp()*1000
                message_tuple = (self.username, self.active_contact, message, result.message_id, time_sent)
                with self._var_lock:
                    self.master_message_list.append(message_tuple)
                self.newMessage.emit("You", message, result.message_id, time_sent)
            else:
                logging.error("Failed to send message")
                # TODO show some ui thing to indicate this error
        except Exception as e:
            logging.error(f"Error sending messsage: {e}")

    # start receive message stream
    def receiveMessage(self):
        logging.info('Receiving message')
        try:
            for message in self.messageStub.subscribeMessages(message_pb2.receiveMessagesRequest(request=True)):
                js_timestamp = (message.sent_at.seconds * 1000) + (message.sent_at.nanos // 1000000)
                message_tuple = (message.sender, message.receiver, message.content, message.messageId, js_timestamp)
                with self._var_lock:
                    self.master_message_list.append(message_tuple)

                if (message.sender == self.active_contact):
                    self.newMessage.emit(message.sender, message.content, message.messageId, js_timestamp)
        except Exception as e:
            logging.error("Receive message thread has errored: {e}")

    # Workout who the selected contact is
    @Slot(str)
    def set_active_contact(self, contact_name):
        with self._var_lock:
            self.active_contact = contact_name
            logging.debug(f"Active contact changed to: {contact_name}")
            # Loop through master message list and add all relevent messages to ui
            for message in self.master_message_list:
                if (message[0] == self.active_contact or message[1] == contact_name):
                    if (message[0] == self.username):
                         self.newMessage.emit("You", message[2], message[3], message[4])
                    else:
                        self.newMessage.emit(message[0], message[2], message[3], message[4])


    # Populate contacts
    def getContacts(self):
        logging.info("Getting list of contacts")
        try:
            request = message_pb2.contactsRequest(request=True)
            get_contacts_result = self.messageStub.getContacts.future(request)
            results = get_contacts_result.result()
            for result in results.contacts:
                if (result.name != self.username):
                    self.addContactSignal.emit(result.name)
            self.set_active_contact(results.contacts[0].name)
        except Exception as e:
            logging.error(f"Error getting contacts: {e}")
