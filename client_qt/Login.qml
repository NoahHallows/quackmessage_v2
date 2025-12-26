import QtQuick
import QtQuick.Controls

Rectangle {
    width: 1920
    height: 1080
    visible: true // This is critical to make the window appear
    //title: "Quackmessage Login"

    LoginForm {
        loginBtn.onClicked: {
            console.log("Login button clicked")
            console.log(usernameEdit.text)
            console.log(passwordEdit.text)
            if (passwordEdit.text.length == 0)
            {
                console.log("Enter a password")
            }
            if (usernameEdit.text.length == 0)
            {
                console.log("Enter a username")
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
            }
            else
            {
                backend.request_email_code(emailEdit.text)
            }
        }

        submitVerificationCode.onClicked: {
            console.log("Verification code submitted")
            console.log(verificationCodeEdit.text)
            if (verificationCodeEdit.text.length == 0)
            {
                console.log("Enter code")
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
            console.log(usernameEdit.text)
            console.log(passwordEdit.text)
            backend.create_account(usernameEdit.text, passwordEdit.text)
        }

    }

}
