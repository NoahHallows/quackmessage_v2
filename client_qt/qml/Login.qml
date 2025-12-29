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
            console.log("Logging in bc login btn was clicked")
            login()
        }

        submitEmailBtn.onClicked: {
            emailCodeRequestFunction()
            verificationCodeEdit.forceActiveFocus()
        }

        submitVerificationCode.onClicked: {
            submitVerificationCodeFunction()
            usernameEdit.forceActiveFocus()
        }

        requestNewCodeBtn.onClicked: {
            backend.request_email_code(emailEdit.text)
            verificationCodeEdit.forceActiveFocus()
        }

        createAccountBtn.onClicked: {
            console.log("Creating account bc create account btn was clicked")
            createAccountFunction()
        }

        usernameEdit.onAccepted: {
            passwordEdit.forceActiveFocus()
        }

        passwordEdit.onAccepted: {
            // TODO check rectangle state so it works for create account
            login()
        }

        emailEdit.onAccepted: {
            emailCodeRequestFunction()
            loginState = "enterEmailVerificationCode"
        }

        verificationCodeEdit.onAccepted: {
            submitVerificationCodeFunction()
            loginState = "createUser"
            usernameEdit.forceActiveFocus()
        }

        selectLoginBtn.onClicked: {
            usernameEdit.forceActiveFocus()
        }

        selectCreateUserBtn.onClicked: {
            emailEdit.forceActiveFocus()
        }




        // Input validation functions
        function login() {
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
                loginForm.isBusy = true
                backend.login(usernameEdit.text, passwordEdit.text)
            }

        }

        function emailCodeRequestFunction(){
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
                    loginForm.isBusy = true
                    backend.request_email_code(emailEdit.text)
                }
                else {
                    loginForm.errorPopup.errorText = "Enter a valid email"
                    loginForm.errorPopup.open()
                    loginForm.loginState = "emailCodeRequest"
                }
            }

        }

        function submitVerificationCodeFunction() {
            if (verificationCodeEdit.text.length == 0)
            {
                loginForm.errorPopup.errorText = "Enter the code"
                loginForm.errorPopup.open()
            }
            else {
                loginForm.isBusy = true
                backend.verify_email_code(Number(verificationCodeEdit.text))
            }

        }

        function createAccountFunction() {
            if (usernameEdit.text.length == 0) {
                loginForm.errorPopup.errorText = "Enter an username"
                loginForm.errorPopup.open()
            }
            else if (passwordEdit.text.length == 0) {
                loginForm.errorPopup.errorText = "Enter a password"
           loginForm.errorPopup.open()
            }
            else {
                loginForm.isBusy = true
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
            }

            function onSendEmailFail() {
                loginForm.errorPopup.errorText = "Unable to send email"
                loginForm.errorPopup.open()
                loginForm.loginState = "emailCodeRequest"
            }
            function onEmailVerificationFail() {
                loginForm.errorPopup.errorText = "Incorrect code"
                loginForm.errorPopup.open()
                loginForm.verificationCodeEdit.clear()
                loginForm.loginState = "enterEmailVerificationCode"
            }
            function onAccountCreationFail() {
                loginForm.errorPopup.errorText = "Error creating account"
                loginForm.errorPopup.open()
                loginForm.passwordEdit.clear()
            }
            function onRequestFinished() {
                loginForm.isBusy = false
            }
        }
    }

}
