from PySide6.QtCore import QObject, Slot, Property, Signal

class Backend(QObject):
    def __init__(self):
        super().__init__()
        self._user_email = ""

    # This allows QML to call a Python function
    @Slot(str, str)
    def login(self, username, password):
        print(f"Attempting login for: {username}")
        # Add your PostgreSQL logic here!

    # This allows Python to send data back to QML
    @Slot(str)
    def request_email_code(self, email):
        print(f"Sending code to: {email}")
        # logic to send email...
        #

    @Slot(int)
    def verify_email_code(self, code):
        print(f"Verification code {code}")

    @Slot(str, str)
    def create_account(self, username, password):
        print("creating user")
