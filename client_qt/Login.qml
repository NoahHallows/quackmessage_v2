import QtQuick
import QtQuick.Controls

Window {
    width: 1920
    height: 1080
    visible: true // This is critical to make the window appear
    title: "Quackmessage Login"

    LoginForm {
        loginBtn.onClicked: {
            console.log("Login button clicked")
            console.log(usernameEdit.text)
            console.log(passwordEdit.text)
            backend.login(usernameEdit.text, passwordEdit.text)
        }
    }

}
