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



class Backend(QObject):
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
        #self.HOST = "192.168.1.150:5555"
        self.HOST = "message.quackmail.com.au:5555"
        self._user_email = ""
        self.username = ""
        self.token = ""
        call_credentials = grpc.access_token_call_credentials(self.token)
        channel_credentials = grpc.ssl_channel_credentials(_credentials.TLS_PUB)
        composite_credentials = grpc.composite_channel_credentials(channel_credentials, call_credentials)
        self.channel = grpc.secure_channel(self.HOST, composite_credentials)
        self.authStub = auth_pb2_grpc.QuackMessageAuthStub(self.channel)
        self.messageStub = message_pb2_grpc.MessagerStub(self.channel)

    # This allows QML to call a Python function
    @Slot(str, str)
    def login(self, username, password):
        print(f"Attempting login for: {username}")
        # Add your PostgreSQL logic here!
        request = auth_pb2.LoginMessage(username=username, password=password)
        login_future = self.authStub.Login.future(request)
        result = login_future.result()
        if result.success == True:
            self.username = username
            self.token = result.auth_token
            # Verify jwt was signed by valid key
            try:
                jwt.decode(result.auth_token, _credentials.JWT_PUB, algorithms=["RS256"])
            except:
                print("ERROR VALIDATING AUTH TOKEN!!\nExiting", file=sys.stderr)
            # Create new channel with auth token in metadata
            call_credentials = grpc.access_token_call_credentials(self.token)
            channel_credentials = grpc.ssl_channel_credentials(_credentials.TLS_PUB)
            composite_credentials = grpc.composite_channel_credentials(channel_credentials, call_credentials)
            self.channel = grpc.secure_channel(self.HOST, composite_credentials)
            self.authStub = auth_pb2_grpc.QuackMessageAuthStub(self.channel)
            self.messageStub = message_pb2_grpc.MessagerStub(self.channel)
            self.loginSuccess.emit()
            # Start receive message stream
            self.receiveMessageThread = threading.Thread(target=self.receiveMessage, args=(), daemon=True)
            self.receiveMessageThread.start()
            getContactsThread = threading.Thread(target=self.getContacts, args=(),daemon=True)
            getContactsThread.start()
            self.setUserName.emit(self.username)
        else:
            self.loginFail.emit()
        self.requestFinished.emit()


    # This allows Python to send data back to QML
    @Slot(str)
    def request_email_code(self, email):
        print(f"Sending code to: {email}")
        # logic to send email...
        request = auth_pb2.VerifyEmailMessage(email=email)
        email_code = self.authStub.VerifyEmail.future(request)
        result = email_code.result()
        print(f"Email sent: {result.emailSent}")
        if result.emailSent == False:
            self.sendEmailFail.emit()
        self.requestFinished.emit()



    @Slot(int)
    def verify_email_code(self, code):
        print(f"Verification code {code}")
        request = auth_pb2.VerificationCodeMessage(code=code)
        verify_result = self.authStub.CheckCode.future(request)
        result = verify_result.result()
        if result.verified == False:
            self.emailVerificationFail.emit()
        self.requestFinished.emit()

    @Slot(str, str)
    def create_account(self, username, password):
        print("creating user")
        request = auth_pb2.CreateUserMessage(username=username, password=password)
        create_account_result = self.authStub.CreateUser.future(request)
        result = create_account_result.result()
        if result.success == True:
            self.token = result.auth_token
            self.username = username
            # Verify jwt was signed by valid key
            """try:
                jwt.decode(result.auth_token, _credentials.JWT_PUB, algorithms=["RS256"])
            except:
                print("ERROR VALIDATING AUTH TOKEN!!\nExiting", file=sys.stderr)
                sys.exit(1)"""
            # Create new channel with auth token in metadata
            call_credentials = grpc.access_token_call_credentials(self.token)
            channel_credentials = grpc.ssl_channel_credentials(_credentials.TLS_PUB)
            composite_credentials = grpc.composite_channel_credentials(channel_credentials, call_credentials)
            self.channel = grpc.secure_channel(self.HOST, composite_credentials)
            self.authStub = auth_pb2_grpc.QuackMessageAuthStub(self.channel)
            self.messageStub = message_pb2_grpc.MessagerStub(self.channel)
            self.loginSuccess.emit()
            # Start receive message stream
            self.receiveMessageThread = threading.Thread(target=self.receiveMessage, args=(), daemon=True)
            self.receiveMessageThread.start()
            getContactsThread = threading.Thread(target=self.getContacts, args=(),daemon=True)
            getContactsThread.start()
            self.setUserName.emit(self.username)

        else:
            self.accountCreationFail.emit()
        self.requestFinished.emit()
    # Message stuff
    @Slot(str)
    def send_message(self, message):
        print(f"Sending {message} to {self.active_contact}")
        request = message_pb2.Message(sender=self.username, receiver=self.active_contact, content=message)
        send_message_result = self.messageStub.sendMessage.future(request)
        result = send_message_result.result()
        print(f"Success: , message id: {result.message_id}")
        if result.sendSuccessful == True:
            time_sent = datetime.now().timestamp()*1000
            message_tuple = (self.username, self.active_contact, message, result.message_id, time_sent)
            self.master_message_list.append(message_tuple)
            self.newMessage.emit("You", message, result.message_id, time_sent)

    # start receive message stream
    def receiveMessage(self):
        print('Receiving message')

        for message in self.messageStub.subscribeMessages(message_pb2.receiveMessagesRequest(request=True)):
            js_timestamp = (message.sent_at.seconds * 1000) + (message.sent_at.nanos // 1000000)
            message_tuple = (message.sender, message.receiver, message.content, message.messageId, js_timestamp)
            self.master_message_list.append(message_tuple)

            if (message.sender == self.active_contact):
                self.newMessage.emit(message.sender, message.content, message.messageId, js_timestamp)

    # Workout who the selected contact is
    @Slot(str)
    def set_active_contact(self, contact_name):
        print(f"Active contact changed to: {contact_name}")
        self.active_contact = contact_name
        # Loop through master message list and add all relevent messages to ui
        for message in self.master_message_list:
            if (message[0] == self.active_contact or message[1] == self.active_contact):
                if (message[0] == self.username):
                     self.newMessage.emit("You", message[2], message[3], message[4])
                else:
                    self.newMessage.emit(message[0], message[2], message[3], message[4])


    # Populate contacts
    def getContacts(self):
        request = message_pb2.contactsRequest(request=True)
        get_contacts_result = self.messageStub.getContacts.future(request)
        results = get_contacts_result.result()
        self.set_active_contact(results.contacts[0].name)
        for result in results.contacts:
            if (result.name != self.username):
                self.addContactSignal.emit(result.name)
