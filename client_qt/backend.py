from PySide6.QtCore import QObject, Slot, Property, Signal
import auth_pb2
import auth_pb2_grpc
import message_pb2
import message_pb2_grpc
import grpc
import _credentials



class Backend(QObject):
    # Auth stuff
    loginSuccess = Signal()
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




    # This allows Python to send data back to QML
    @Slot(str)
    def request_email_code(self, email):
        print(f"Sending code to: {email}")
        # logic to send email...
        request = auth_pb2.VerifyEmailMessage(email=email)
        email_code = self.authStub.VerifyEmail.future(request)
        result = email_code.result()
        print(f"Email sent: {result.emailSent}")


    @Slot(int)
    def verify_email_code(self, code):
        print(f"Verification code {code}")
        request = auth_pb2.VerificationCodeMessage(code=code)
        verify_result = self.authStub.CheckCode.future(request)
        result = verify_result.result()
        print(f"Result: {result.verified}")

    @Slot(str, str)
    def create_account(self, username, password):
        print("creating user")
        request = auth_pb2.CreateUserMessage(username=username, password=password)
        create_account_result = self.authStub.CreateUser.future(request)
        result = create_account_result.result()
        print(f"Result {result.success}, {result.auth_token}")

    # Message stuff
    @Slot(str, str)
    def send_message(self, receiver, message):
        print(f"Sending {message} to {receiver}")
        request = message_pb2.Message(sender=self.username, receiver=receiver, content=message)
        send_message_result = self.messageStub.sendMessage.future(request)
        result = send_message_result.result()
        print(f"Success: , message id: {result.message_id}")
