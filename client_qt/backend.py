from PySide6.QtCore import QObject, Slot, Property, Signal
import auth_pb2
import auth_pb2_grpc
import message_pb2
import message_pb2_grpc
import grpc
import _credentials
import threading


class Backend(QObject):
    # Signals
    loginSuccess = Signal()
    newMessage = Signal(str, str, int)
    loginFail = Signal()
    sendEmailFail = Signal()
    emailVerificationFail = Signal()
    accountCreationFail = Signal()
    addContactSignal = Signal(str)
    active_contact = ""
    master_message_list = []
    # Auth stuff
    def __init__(self):
        super().__init__()
        self.HOST = "localhost:5555"
        self._user_email = ""
        self.username = ""
        self.token = ""
        call_credentials = grpc.access_token_call_credentials(self.token)
        channel_credentials = grpc.ssl_channel_credentials(_credentials.ROOT_CERTIFICATE)
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
        print(f"Result: {result.success}, auth token = {result.auth_token}")
        if result.success == True:
            self.username = username
            self.token = result.auth_token
            call_credentials = grpc.access_token_call_credentials(self.token)
            channel_credentials = grpc.ssl_channel_credentials(_credentials.ROOT_CERTIFICATE)
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
        else:
            self.loginFail.emit()


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



    @Slot(int)
    def verify_email_code(self, code):
        print(f"Verification code {code}")
        request = auth_pb2.VerificationCodeMessage(code=code)
        verify_result = self.authStub.CheckCode.future(request)
        result = verify_result.result()
        print(f"Result: {result.verified}")
        if result.verified == False:
            self.emailVerificationFail.emit()

    @Slot(str, str)
    def create_account(self, username, password):
        print("creating user")
        request = auth_pb2.CreateUserMessage(username=username, password=password)
        create_account_result = self.authStub.CreateUser.future(request)
        result = create_account_result.result()
        print(f"Result {result.success}, {result.auth_token}")
        if result.success == False:
            self.accountCreationFail.emit()

    # Message stuff
    @Slot(str)
    def send_message(self, message):
        print(f"Sending {message} to {self.active_contact}")
        request = message_pb2.Message(sender=self.username, receiver=self.active_contact, content=message)
        send_message_result = self.messageStub.sendMessage.future(request)
        result = send_message_result.result()
        print(f"Success: , message id: {result.message_id}")
        if result.sendSuccessful == True:
            message_tuple = (self.username, self.active_contact, message, result.message_id)
            self.master_message_list.append(message_tuple)

    # start receive message stream
    def receiveMessage(self):
        print('Receiving message')

        for message in self.messageStub.subscribeMessages(message_pb2.receiveMessagesRequest(request=True)):
            message_tuple = (message.sender, message.receiver, message.content, message.messageId)
            self.master_message_list.append(message_tuple)
            if (message.sender == self.active_contact):
                self.newMessage.emit(message.sender, message.content, message.messageId)

    # Workout who the selected contact is
    @Slot(str)
    def set_active_contact(self, contact_name):
        print(f"Active contact changed to: {contact_name}")
        self.active_contact = contact_name
        # Loop through master message list and add all relevent messages to ui
        for message in self.master_message_list:
            if (message[0] == self.active_contact or message[1] == self.active_contact):
                if (message[0] == self.username):
                     self.newMessage.emit("You", message[2], message[3])
                else:
                    self.newMessage.emit(message[0], message[2], message[3])


    # Populate contacts
    def getContacts(self):
        request = message_pb2.contactsRequest(request=True)
        get_contacts_result = self.messageStub.getContacts.future(request)
        results = get_contacts_result.result()
        for result in results.contacts:
            if (result.name != self.username):
                self.addContactSignal.emit(result.name)
