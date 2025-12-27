import QtQuick
import QtQuick.Controls

Rectangle {
    width: 250
    height: 500
    visible: true // This is critical to make the window appear
    //title: "Quackmessage Login"

    LoginForm {
        id: loginForm
        loginBtn.onClicked: {
            console.log("Login button clicked")
            console.log(usernameEdit.text.length)
            console.log(passwordEdit.text.length)
            if (passwordEdit.text.length == 0)
            {
                console.log("Enter a password")
                loginForm.errorPopup.errorText = "Enter a password"
                loginForm.errorPopup.open()
            }
            else if (usernameEdit.text.length == 0)
            {
                console.log("Enter a username")
                loginForm.errorPopup.errorText = "Enter an username"
                loginForm.errorPopup.open()
            }
            else
            {
                backend.login(usernameEdit.text, passwordEdit.text)
            }

        }

        submitEmailBtn.onClicked: {
            console.log("Submit email button clicked")
            console.log(emailEdit.text)
            if (emailEdit.text.length == 0)
            {
                console.log("Enter an email")
                loginForm.errorPopup.errorText = "Enter a valid email"
                loginForm.errorPopup.open()
                loginForm.loginState = "emailCodeRequest"
            }
            else
            {
                const pattern = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
                if (pattern.test(emailEdit.text.toLowerCase())) {
                    backend.request_email_code(emailEdit.text)
                }
                else {
                    loginForm.errorPopup.errorText = "Enter a valid email"
                    loginForm.errorPopup.open()
                    loginForm.loginState = "emailCodeRequest"
                }
            }
        }

        submitVerificationCode.onClicked: {
            console.log("Verification code submitted")
            console.log(verificationCodeEdit.text)
            if (verificationCodeEdit.text.length == 0)
            {
                console.log("Enter code")
                loginForm.errorPopup.errorText = "Enter the code"
                loginForm.errorPopup.open()
            }
            else {
                backend.verify_email_code(Number(verificationCodeEdit.text))
            }
        }

        requestNewCodeBtn.onClicked: {
            console.log("New code requested")
            console.log(emailEdit.text)
            backend.request_email_code(emailEdit.text)
        }

        createAccountBtn.onClicked: {
            console.log("Create account button clicked")
            if (usernameEdit.text.length == 0) {
                loginForm.errorPopup.errorText = "Enter an username"
                loginForm.errorPopup.open()
            }
            else if (passwordEdit.text.length == 0) {
                loginForm.errorPopup.errorText = "Enter a password"
                loginForm.errorPopup.open()
            }
            else {
                backend.create_account(usernameEdit.text, passwordEdit.text)
            }
        }

        Connections {
            // These are triggered by signals from backend.py
            target: backend
            function onLoginFail(message) {
                loginForm.errorPopup.errorText = "Incorrect username or password"
                loginForm.errorPopup.open()
                loginForm.passwordEdit.clear()
                loginForm.loginRectangle.state = "login"
            }

            function onSendEmailFail() {
                loginForm.errorPopup.errorText = "Unable to send email"
                loginForm.errorPopup.open()
                loginForm.loginRectangle.state = "emailCodeRequest"
            }
            function onEmailVerificationFail() {
                loginForm.errorPopup.errorText = "Incorrect code"
                loginForm.errorPopup.open()
                loginForm.verificationCodeEdit.clear()
                loginForm.loginRectangle.state = "enterEmailVerificationCode"
            }
            function onAccountCreationFail() {
                loginForm.errorPopup.errorText = "Error creating account"
                loginForm.errorPopup.open()
                loginForm.passwordEdit.clear()
                loginForm.loginRectangle.state = "createUser"
            }
        }
    }

}
