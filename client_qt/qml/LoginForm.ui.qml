

/*
This is a UI file (.ui.qml) that is intended to be edited in Qt Design Studio only.
It is supposed to be strictly declarative and only uses a subset of QML. If you edit
this file manually, you might introduce QML code that is not supported by Qt Design Studio.
Check out https://doc.qt.io/qtcreator/creator-quick-ui-forms.html for details on .ui.qml files.
*/
import QtQuick
import QtQuick.Window
import QtQuick.Controls

//import Quackmessage_desktop
//import QtQuick.Studio.DesignEffects
Rectangle {
    id: rectangle
    width: 700
    height: 700
    state: "initial"
    color: "#272727"

    // Allow login.qml to see and change these properties
    property alias loginBtn: loginButton
    property alias usernameEdit: usernameEdit
    property alias passwordEdit: passwordEdit
    property alias selectLoginBtn: selectLoginButton
    property alias selectCreateUserBtn: selectCreateUserButton
    property alias emailEdit: emailEdit
    property alias submitEmailBtn: submitEmailButton
    property alias requestNewCodeBtn: requestNewCodeButton
    property alias createAccountBtn: createAccountButton
    property alias verificationCodeEdit: verificationCodeEdit
    property alias submitVerificationCode: submitVerificationCode
    property alias errorPopup: errorPopup
    property alias loginState: rectangle.state

    Text {
        id: title
        x: 100
        y: 100
        width: 275
        height: 136
        color: "#ffffff"
        text: qsTr("Quackmessage\nLogin")
        font.pixelSize: 30
        horizontalAlignment: Text.AlignHCenter
    }

    Text {
        id: userNameLabel
        x: 100
        y: 250
        width: 90
        height: 30
        opacity: 0
        color: "#ffffff"
        text: qsTr("Username")
        font.pixelSize: 14
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
        enabled: false
    }

    TextField {
        id: usernameEdit
        x: 250
        y: 250
        width: 145
        height: 30
        opacity: 0
        enabled: false
        placeholderText: qsTr("Username")
        background: Rectangle {
            implicitWidth: 145
            implicitHeight: 30
            opacity: enabled ? 1 : 0.3
            color: "#888e95"
            border.color: "#ffffff"
            border.width: 1
            radius: 2
        }
    }

    Text {
        id: passwordLabel
        x: 100
        y: 310
        width: 90
        height: 30
        opacity: 0
        color: "#ffffff"
        text: qsTr("Password")
        font.pixelSize: 14
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
        enabled: false
    }

    TextField {
        id: passwordEdit
        x: 250
        y: 310
        width: 145
        height: 30
        opacity: 0
        echoMode: TextInput.Password
        enabled: false
        placeholderText: qsTr("Password")
        background: Rectangle {
            implicitWidth: 145
            implicitHeight: 30
            opacity: enabled ? 1 : 0.3
            color: "#888e95"
            border.color: "#ffffff"
            border.width: 1
            radius: 2
        }
    }

    Button {
        id: loginButton
        x: 190
        y: 450
        opacity: 1
        text: qsTr("Login")
        background: Rectangle {
            implicitWidth: 100
            implicitHeight: 40
            opacity: enabled ? 1 : 0.3
            color: "#0072ff"
            border.color: "#ffffff"
            border.width: 1
            radius: 2
        }
    }

    Button {
        id: selectLoginButton
        x: 100
        y: 400
        visible: true
        text: qsTr("Login")
        enabled: true
        onClicked: rectangle.state = "login"
        background: Rectangle {
            implicitWidth: 100
            implicitHeight: 40
            opacity: enabled ? 1 : 0.3
            color: "#0072ff"
            border.color: "#ffffff"
            border.width: 1
            radius: 2
        }
    }

    Button {
        id: selectCreateUserButton
        x: 270
        y: 400
        visible: true
        text: qsTr("Create account")
        enabled: true
        onClicked: rectangle.state = "emailCodeRequest"
        background: Rectangle {
            implicitWidth: 100
            implicitHeight: 40
            opacity: enabled ? 1 : 0.3
            color: "#007429"
            border.color: "#ffffff"
            border.width: 1
            radius: 2
        }
    }

    TextField {
        id: emailEdit
        x: 200
        y: 300
        width: 250
        height: 30
        opacity: 0
        visible: true
        placeholderText: qsTr("Email")
        enabled: false
        background: Rectangle {
            opacity: enabled ? 1 : 0.3
            color: "#888e95"
            radius: 2
            border.color: "#ffffff"
            border.width: 1
            implicitWidth: 250
            implicitHeight: 30
        }
    }

    Text {
        id: emailLabel
        x: 70
        y: 300
        width: 125
        height: 30
        opacity: 0
        color: "#ffffff"
        text: qsTr("Enter your email:")
        font.pixelSize: 14
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
        enabled: false
    }

    Button {
        id: submitEmailButton
        x: 180
        y: 400
        opacity: 0
        text: qsTr("Request code")
        onClicked: rectangle.state = "enterEmailVerificationCode"
        background: Rectangle {
            opacity: enabled ? 1 : 0.3
            color: "#0d60a9"
            radius: 2
            border.color: "#ffffff"
            border.width: 1
            implicitWidth: 100
            implicitHeight: 40
        }
    }

    TextField {
        id: verificationCodeEdit
        x: 220
        y: 365
        width: 175
        height: 30
        opacity: 0
        placeholderText: qsTr("Code")
        enabled: false
        background: Rectangle {
            opacity: enabled ? 1 : 0.3
            color: "#888e95"
            radius: 2
            border.color: "#ffffff"
            border.width: 1
            implicitWidth: 250
            implicitHeight: 30
        }
    }

    Text {
        id: verificationCodeLabel
        x: 112
        y: 276
        width: 277
        height: 36
        opacity: 0
        color: "#ffffff"
        text: qsTr("A verification code was sent to your email")
        font.pixelSize: 14
        enabled: false
    }

    Button {
        id: submitVerificationCode
        x: 290
        y: 500
        opacity: 0
        visible: true
        text: qsTr("Submit")
        onClicked: rectangle.state = "createUser"
        background: Rectangle {
            opacity: enabled ? 1 : 0.3
            color: "#0da91f"
            radius: 2
            border.color: "#ffffff"
            border.width: 1
            implicitWidth: 100
            implicitHeight: 40
        }
    }

    Button {
        id: requestNewCodeButton
        x: 75
        y: 500
        opacity: 0
        visible: true
        text: qsTr("Request new code")
        background: Rectangle {
            opacity: enabled ? 1 : 0.3
            color: "#deb605"
            radius: 2
            border.color: "#ffffff"
            border.width: 1
            implicitWidth: 100
            implicitHeight: 40
        }
    }

    Button {
        id: createAccountButton
        x: 190
        y: 450
        opacity: 0
        text: qsTr("Create account")
        background: Rectangle {
            opacity: enabled ? 1 : 0.3
            color: "#0072ff"
            radius: 2
            border.color: "#000000"
            border.width: 1
            implicitWidth: 100
            implicitHeight: 40
        }
    }

    BusyIndicator {
        id: busyIndicator
        x: 223
        y: 365
        width: 55
        height: 48
        visible: false
    }

    Button {
        id: backButton
        x: 50
        y: 192
        opacity: 0
        onClicked: rectangle.state = "initial"
        text: qsTr("Back")
        enabled: false
    }

    Text {
        id: verificationCodeLabel1
        x: 100
        y: 365
        width: 100
        height: 30
        opacity: 0
        color: "#ffffff"
        text: qsTr("Enter code:")
        font.pixelSize: 14
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
    }

    // Error popup
    Popup {
        id: errorPopup
        x: 100
        y: 350
        width: 300
        height: 100
        modal: true
        focus: true
        closePolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutsideParent
        property alias errorText: errorLabel.text
        background: Rectangle {
            color: "#1e1e1e"
            border.color: "#ff4444"
            border.width: 2
            radius: 10
        }

        Column {
            anchors.centerIn: parent
            spacing: 20

            Text {
                id: errorLabel
                text: qsTr("Invalid credentials")
                color: "white"
                font.pixelSize: 16
                horizontalAlignment: Text.AlignHCenter
            }

            Button {
                text: qsTr("OK")
                anchors.horizontalCenter: parent.horizontalCenter
                onClicked: errorPopup.close()
            }
        }
    }

    states: [
        State {
            name: "initial"
            PropertyChanges {
                target: userNameLabel
                enabled: false
                opacity: 0
                scale: 1.0
            }
            PropertyChanges {
                target: usernameEdit
                enabled: false
                opacity: 0
                scale: 1.0
            }
            PropertyChanges {
                target: passwordEdit
                enabled: false
                opacity: 0
                scale: 1.0
            }
            PropertyChanges {
                target: passwordLabel
                enabled: false
                opacity: 0
                scale: 1.0
            }
            PropertyChanges {
                target: loginButton
                enabled: false
                opacity: 0
                scale: 1.0
            }
            PropertyChanges {
                target: selectCreateUserButton
                enabled: true
                opacity: 1
                scale: 1.0
            }
            PropertyChanges {
                target: selectLoginButton
                enabled: true
                opacity: 1
                scale: 1.0
            }
            PropertyChanges {
                target: createAccountButton
                enabled: false
                opacity: 0
                visible: false
            }
            PropertyChanges {
                target: emailLabel
                enabled: false
                opacity: 0
                scale: 1.0
            }
            PropertyChanges {
                target: emailEdit
                enabled: false
                opacity: 0
                scale: 1.0
            }
            PropertyChanges {
                target: submitEmailButton
                enabled: false
                opacity: 0
                scale: 1.0
            }
            PropertyChanges {
                target: emailLabel
                enabled: false
                opacity: 0
                scale: 1.0
            }
            PropertyChanges {
                target: emailEdit
                enabled: false
                opacity: 0
                scale: 1.0
            }
            PropertyChanges {
                target: submitEmailButton
                enabled: false
                opacity: 0
                scale: 1.0
            }
            PropertyChanges {
                target: verificationCodeEdit
                enabled: false
                opacity: 0
                scale: 1.0
            }
            PropertyChanges {
                target: verificationCodeLabel
                enabled: false
                opacity: 0
                scale: 1.0
            }
            PropertyChanges {
                target: submitVerificationCode
                enabled: false
                opacity: 0
                scale: 1.0
            }
            PropertyChanges {
                target: requestNewCodeButton
                enabled: false
                opacity: 0
                scale: 1.0
            }
            PropertyChanges {
                target: backButton
                enabled: false
                opacity: 0
                scale: 1.0
            }

        },

        State {
            name: "login"
            PropertyChanges {
                target: userNameLabel
                enabled: true
                opacity: 1
                scale: 1.0
            }
            PropertyChanges {
                target: usernameEdit
                enabled: true
                opacity: 1
                scale: 1.0
            }
            PropertyChanges {
                target: passwordEdit
                enabled: true
                opacity: 1
                scale: 1.0
            }
            PropertyChanges {
                target: passwordLabel
                enabled: true
                opacity: 1
                scale: 1.0
            }
            PropertyChanges {
                target: loginButton
                enabled: true
                opacity: 1
                scale: 1.0
            }
            PropertyChanges {
                target: selectCreateUserButton
                enabled: false
                opacity: 0
                scale: 1.0
            }
            PropertyChanges {
                target: selectLoginButton
                enabled: false
                opacity: 0
                scale: 1.0
            }
            PropertyChanges {
                target: createAccountButton
                enabled: false
                opacity: 0
                visible: false
            }
            PropertyChanges {
                target: backButton
                enabled: true
                opacity: 1
                scale: 1.0
            }

        },

        State {
            name: "createUser"
            PropertyChanges {
                target: userNameLabel
                enabled: true
                opacity: 1
                scale: 1.0
            }
            PropertyChanges {
                target: usernameEdit
                enabled: true
                opacity: 1
                scale: 1.0
            }
            PropertyChanges {
                target: passwordEdit
                enabled: true
                opacity: 1
                scale: 1.0
            }
            PropertyChanges {
                target: passwordLabel
                enabled: true
                opacity: 1
                scale: 1.0
            }
            PropertyChanges {
                target: createAccountButton
                enabled: true
                opacity: 1
                scale: 1.0
            }
            PropertyChanges {
                target: verificationCodeEdit
                enabled: false
                opacity: 0
                scale: 1.0
            }
            PropertyChanges {
                target: verificationCodeLabel
                enabled: false
                opacity: 0
                scale: 1.0
            }
            PropertyChanges {
                target: submitVerificationCode
                enabled: false
                opacity: 0
                scale: 1.0
            }
            PropertyChanges {
                target: requestNewCodeButton
                enabled: false
                opacity: 0
                scale: 1.0
            }
            PropertyChanges {
                target: selectCreateUserButton
                enabled: false
                opacity: 0
                scale: 1.0
            }
            PropertyChanges {
                target: selectLoginButton
                enabled: false
                opacity: 0
                scale: 1.0
            }
            PropertyChanges {
                target: backButton
                enabled: true
                opacity: 1
                scale: 1.0
            }

        },

        State {
            name: "emailCodeRequest"
            PropertyChanges {
                target: emailLabel
                enabled: true
                opacity: 1
                scale: 1.0
            }
            PropertyChanges {
                target: emailEdit
                enabled: true
                opacity: 1
                scale: 1.0
            }
            PropertyChanges {
                target: submitEmailButton
                enabled: true
                opacity: 1
                scale: 1.0
            }
            PropertyChanges {
                target: selectCreateUserButton
                enabled: false
                opacity: 0
                scale: 1.0
            }
            PropertyChanges {
                target: selectLoginButton
                enabled: false
                opacity: 0
                scale: 1.0
            }
            PropertyChanges {
                target: backButton
                enabled: true
                opacity: 1
                scale: 1.0
            }
            PropertyChanges {
                target: loginButton
                enabled: false
                opacity: 0
                scale: 1.0
            }

        },

        State {
            name: "enterEmailVerificationCode"
            PropertyChanges {
                target: emailLabel
                enabled: false
                opacity: 0
                scale: 1.0
            }
            PropertyChanges {
                target: emailEdit
                enabled: false
                opacity: 0
                scale: 1.0
            }
            PropertyChanges {
                target: submitEmailButton
                enabled: false
                opacity: 0
                scale: 1.0
            }
            PropertyChanges {
                target: verificationCodeEdit
                enabled: true
                opacity: 1
                scale: 1.0
            }
            PropertyChanges {
                target: verificationCodeLabel
                enabled: true
                opacity: 1
                scale: 1.0
            }
            PropertyChanges {
                target: submitVerificationCode
                enabled: true
                opacity: 1
                scale: 1.0
            }
            PropertyChanges {
                target: requestNewCodeButton
                enabled: true
                opacity: 1
                scale: 1.0
            }
            PropertyChanges {
                target: selectCreateUserButton
                enabled: false
                opacity: 0
                scale: 1.0
            }
            PropertyChanges {
                target: selectLoginButton
                enabled: false
                opacity: 0
                scale: 1.0
            }
            PropertyChanges {
                target: backButton
                enabled: true
                opacity: 1
                scale: 1.0
            }
            PropertyChanges {
                target: loginButton
                enabled: false
                opacity: 0
                scale: 1.0
            }
        }
    ]

    transitions: Transition {
        NumberAnimation {
            properties: "opacity,scale"
            duration: 100
            easing.type: Easing.OutCubic
        }
    }
}



