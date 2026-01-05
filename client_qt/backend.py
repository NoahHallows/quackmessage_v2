from PySide6.QtCore import QObject, Slot, Property, Signal
import auth_pb2
import auth_pb2_grpc
import message_pb2
import message_pb2_grpc
import _credentials
import grpc
import threading
from datetime import datetime, timezone
import jwt
import sys
import logging
# To copy dict and actually make a new one instead of a new reference to the same one
from copy import deepcopy
import operator

ISSUER = "Quackmessage"
AUDIENCE = "Quackmessage_app"

logging.basicConfig(
    format="{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
    level=logging.DEBUG,
)

VERSION = "0.0.0.1"

epoch = datetime(1970, 1, 1)
js_timestamp_epoch = int(epoch.replace(tzinfo=timezone.utc).timestamp() * 1000)
logging.debug(js_timestamp_epoch)
class Backend(QObject):
    logging.info("Starting")
    # Lock for updating class wide variables
    _var_lock = threading.Lock()
    _stub_lock = threading.Lock()
    # Signals
    loginSuccess = Signal()
    newMessageActive = Signal(str, str, int, 'qint64', 'qint64',)
    newMessageDeactive = Signal(str)
    loginFail = Signal()
    sendEmailFail = Signal()
    emailVerificationFail = Signal()
    accountCreationFail = Signal()
    addContactSignal = Signal(str)
    setUserName = Signal(str)
    requestFinished = Signal()
    messageSeen = Signal(int, 'qint64')
    active_contact = ""
    email = ""
    master_message_dict = {}
    # System notifications
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
            #
        # Check version
        request = auth_pb2.ClientVersion(version=VERSION)
        version_future = self.authStub.CheckVersion.future(request)
        result = version_future.result()
        if (result.valid != True):
            logging.error(f"Invalid version, please update to {result.valid_version_num}")
            sys.exit(1)

    def _update_channel(self, token: str) -> None:
        logging.info("Updating channel")
        # Creates new channel and stub
        # Used to update auth token
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
    def login(self, username: str, password: str) -> None:
        logging.info("Login function called, starting helper thread")
        # Start login helper function so we don't block the main ui thread
        threading.Thread(target=self._login_helper, args=(username, password), daemon=True).start()

    # We're back to helper functions again
    def _login_helper(self, username: str, password: str) -> None:
        logging.info(f"Attempting login for: {username}")
        try:
            request = auth_pb2.LoginMessage(username=username, password=password)
            login_future = self.authStub.Login.future(request)
            result = login_future.result()
            if result.success is True:
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
    def request_email_code(self, email: str) -> None:
        logging.info("Email verification code requested")
        threading.Thread(target=self._request_email_helper, args=(email,), daemon=True).start()

    def _request_email_helper(self, email: str) -> None:
        logging.debug(f"Sending code to: {email}")
        try:
            with self._var_lock:
                self.email = email
            request = auth_pb2.VerifyEmailMessage(email=email)
            email_code = self.authStub.VerifyEmail.future(request)
            result = email_code.result()
            logging.debug(f"Email sent: {result.emailSent}")
            if not result.emailSent:
                logging.warning("Error sending email")
                self.sendEmailFail.emit()
        except Exception as e:
            logging.error(f"Error sending email: {e}")
            self.sendEmailFail.emit()
        finally:
            self.requestFinished.emit()



    @Slot(int)
    def verify_email_code(self, code: int) -> None:
        logging.info("Verify email code function has been called")
        threading.Thread(target=self._verify_email_helper, args=(code,), daemon=True).start()

    def _verify_email_helper(self, code: int) -> None:
        logging.debug(f"Verification code {code}")
        try:
            with self._var_lock:
                request = auth_pb2.VerificationCodeMessage(code=code, email=self.email)
            verify_result = self.authStub.CheckCode.future(request)
            result = verify_result.result()
            if not result.verified:
                logging.info("Verification has failed, likely wrong code was entered")
                self.emailVerificationFail.emit()
        except Exception as e:
            logging.error(f"Error verifying code: {e}")
            self.emailVerificationFail.emit()
        finally:
            self.requestFinished.emit()

    @Slot(str, str)
    def create_account(self, username: str, password: str) -> None:
        logging.info("Creating user")
        threading.Thread(target=self._create_account_helper, args=(username, password), daemon=False).start()

    def _create_account_helper(self, username: str, password: str) -> None:
        logging.debug(f"Create account helper: {username}, {password}")
        try:
            request = auth_pb2.CreateUserMessage(username=username, password=password, email=self.email)
            create_account_result = self.authStub.CreateUser.future(request)
            result = create_account_result.result()
            if result.success is True:
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
    def send_message(self, message: str) -> None:
        logging.debug(f"Sending {message} to {self.active_contact}")
        try:
            request = message_pb2.Message(sender=self.username, receiver=self.active_contact, content=message)
            send_message_result = self.messageStub.sendMessage.future(request)
            result = send_message_result.result()
            logging.debug(f"Success: {result.sendSuccessful}, message id: {result.message_id}")
            if result.sendSuccessful:
                time_sent = int(datetime.now().timestamp()*1000)
                with self._var_lock:
                    self.master_message_dict[result.message_id] = (self.username,
                                                                   self.active_contact, message,
                                                                   time_sent, js_timestamp_epoch)
                self.newMessageActive.emit("You", message, result.message_id, time_sent, js_timestamp_epoch)
            else:
                logging.error("Failed to send message")
                # TODO show some ui thing to indicate this error
        except Exception as e:
            logging.error(f"Error sending messsage: {e}")

    # start receive message stream
    def receiveMessage(self) -> None:
        logging.info('Receiving message')
        try:
            for message in self.messageStub.subscribeMessages(message_pb2.receiveMessagesRequest(request=True)):
                js_timestamp_sent = int((message.sent_at.seconds * 1000) + (message.sent_at.nanos // 1000000))
                js_timestamp_seen = int((message.seen_at.seconds * 1000) + (message.seen_at.nanos //1000000))
                logging.debug("Message received")
                with self._var_lock:
                    if message.messageId in self.master_message_dict:
                        # Update seen
                        message_tuple = (self.master_message_dict[message.messageId][0],
                                         self.master_message_dict[message.messageId][1],
                                         self.master_message_dict[message.messageId][2],
                                         self.master_message_dict[message.messageId][3], js_timestamp_seen)
                        self.master_message_dict[message.messageId] = message_tuple
                        new_message = False
                        logging.debug("Update seen message")
                    else:
                        # Actual new message
                        self.master_message_dict[message.messageId] = (message.sender, message.receiver, message.content,                                                              js_timestamp_sent, js_timestamp_seen)
                        new_message = True
                        logging.debug("New message (not update seen)")
                if (message.sender == self.active_contact):
                    if new_message:
                        self.newMessageActive.emit(message.sender, message.content, message.messageId, js_timestamp_sent, js_timestamp_seen)
                    if js_timestamp_seen != js_timestamp_epoch and not new_message:
                        logging.debug(f"Emitting update seen for message {message.messageId}")
                        self.messageSeen.emit(message.messageId, js_timestamp_seen)

                else:
                    if js_timestamp_seen == js_timestamp_epoch:
                        logging.debug("Emitting message for deactive sender")
                        self.newMessageDeactive.emit(message.sender)
                    else:
                        logging.debug("Not emitting for deactive sender as read time not epoch")
        except Exception as e:
            logging.error(f"Receive message thread has errored: {e}")




    # Workout who the selected contact is
    @Slot(str)
    def set_active_contact(self, contact_name: str) -> None:
        with self._var_lock:
            self.active_contact = contact_name
            logging.debug(f"Active contact changed to: {contact_name}")
            logging.debug(f"self.username: {self.username}")
            # Loop through master message list and add all relevent messages to ui
            # The tuple is: (sender, receiver, content, time_sent, time_seen)
            sorted_messages = dict(sorted(self.master_message_dict.items(), key=operator.itemgetter(0)))
            logging.debug("Sorted message list follows:")
            for message_id, message in sorted_messages.items():
                logging.debug(f"message id {message_id}: time sent {message[3]}")
                if (message[0] == contact_name or message[1] == contact_name):
                    if (message[0] == self.username):
                         self.newMessageActive.emit("You", message[2], message_id, message[3],
                                                    message[4])
                    else:
                        self.newMessageActive.emit(message[0], message[2], message_id, message[3],
                                                   message[4])
        # Start thread to update seen status on all these messages
        threading.Thread(target=self.update_seen_on_contact_change, args=(contact_name,), daemon=False).start()

    def update_seen_on_contact_change(self, contact_name: str) -> None:
        with self._var_lock:
            master_message_dict_shadow = deepcopy(self.master_message_dict)
            contact_name = deepcopy(self.active_contact)
        time_seen = datetime.now()
        time_seen = time_seen.replace(tzinfo=timezone.utc)
        try:
            for message_id, message in master_message_dict_shadow.items():
                if message[0] == contact_name: # Don't update seen status for messages you sent
                    # Check if it already has a seen time, if so don't update
                    logging.debug(f'message: {message[4]}')
                    logging.debug(f'epoch: {js_timestamp_epoch}')
                    if message[4] == js_timestamp_epoch:
                        request = message_pb2.updateSeen(messageId=message_id, seen_at=time_seen)
                        update_seen_result = self.messageStub.messageSeen.future(request).result()
                        if update_seen_result.success is not True:
                            logging.error(f"Failed to update seen status for message {message_id}")
                    else:
                        logging.debug("Not updating seen as seen not equal to epoch (already seen)")
        except Exception as e:
            logging.error(f"Error setting seen status on {message_id}: {e}")


    # Populate contacts
    def getContacts(self) -> None:
        logging.info("Getting list of contacts")
        try:
            request = message_pb2.contactsRequest(request=True)
            get_contacts_result = self.messageStub.getContacts.future(request)
            results = get_contacts_result.result()
            for result in results.contacts:
                if (result.name != self.username):
                    self.addContactSignal.emit(result.name)
            self.setUserName.emit(self.username)
        except Exception as e:
            logging.error(f"Error getting contacts: {e}")
