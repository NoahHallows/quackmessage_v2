from PySide6.QtCore import QObject, Slot, Property, Signal
import quackmessage_pb2
import quackmessage_pb2_grpc
import grpc

class Backend(QObject):
    def __init__(self):
        super().__init__()
        self._user_email = ""
        self.channel = grpc.insecure_channel('localhost:5555')
        self.stub = quackmessage_pb2_grpc.QuackMessageAuthStub(self.channel)

    # This allows QML to call a Python function
    @Slot(str, str)
    def login(self, username, password):
        print(f"Attempting login for: {username}")
        # Add your PostgreSQL logic here!
        request = quackmessage_pb2.LoginMessage(username=username, password=password)
        login_future = self.stub.Login.future(request)
        result = login_future.result()
        print(f"Result: {result.success}, auth token = {result.auth_token}")

    # This allows Python to send data back to QML
    @Slot(str)
    def request_email_code(self, email):
        print(f"Sending code to: {email}")
        # logic to send email...
        request = quackmessage_pb2.VerifyEmailMessage(email=email)
        email_code = self.stub.VerifyEmail.future(request)
        result = email_code.result()
        print(f"Email sent: {result.emailSent}")


    @Slot(int)
    def verify_email_code(self, code):
        print(f"Verification code {code}")
        request = quackmessage_pb2.VerificationCodeMessage(code=code)
        verify_result = self.stub.CheckCode.future(request)
        result = verify_result.result()
        print(f"Result: {result.verified}")

    @Slot(str, str)
    def create_account(self, username, password):
        print("creating user")
        request = quackmessage_pb2.CreateUserMessage(username=username, password=password)
        create_account_result = self.stub.CreateUser(request)
        result = create_account_result.result()
        print(f"Result {result.success}, {result.auth_token}")
