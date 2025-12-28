import QtQuick
import QtQuick.Window
import QtQuick.Controls

Rectangle {
    id: rectangle
    width: 700
    height: 700
    state: "initial"
    color: "#272727"

    property string borderColor: "#aaaaaa"
    property string blueColor: "#0072ff"
    property string greenColor: "#007429"
    property string placeHolderTextColor: "#b6b6b6"

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
        x: 350 - (width / 2)
        y: 100
        width: 275
        height: 136
        color: "#ffffff"
        text: qsTr("Quackmessage\nLogin")
        font.pixelSize: 30
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
    }

    Text {
        id: userNameLabel
        x: 275 - (width / 2)
        y: 300
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
        x: 425 - (width / 2)
        y: 300
        width: 145
        height: 30
        opacity: 0
        wrapMode: Text.Wrap
        placeholderTextColor: placeHolderTextColor
        enabled: false
        placeholderText: qsTr("Username")
        background: Rectangle {
            implicitWidth: 145
            implicitHeight: 30
            opacity: enabled ? 1 : 0.3
            color: "#888e95"
            border.color: borderColor
            border.width: 1
            radius: 2
        }
    }

    Text {
        id: passwordLabel
        x: 275 - (width / 2)
        y: 360
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
        x: 425 - (width / 2)
        y: 360
        width: 145
        height: 30
        opacity: 0
        wrapMode: Text.Wrap
        placeholderTextColor: placeHolderTextColor
        echoMode: TextInput.Password
        enabled: false
        placeholderText: qsTr("Password")
        background: Rectangle {
            implicitWidth: 145
            implicitHeight: 30
            opacity: enabled ? 1 : 0.3
            color: "#888e95"
            border.color: borderColor
            border.width: 1
            radius: 2
        }
    }

    Button {
        id: loginButton
        x: 350 - (width / 2)
        y: 450
        opacity: 0
        text: qsTr("Login")
        background: Rectangle {
            implicitWidth: 100
            implicitHeight: 40
            opacity: enabled ? 1 : 0.3
            color: blueColor
            border.color: borderColor
            border.width: 1
            radius: 8
        }
    }

    Button {
        id: selectLoginButton
        x: 250 - (width / 2)
        y: 450
        visible: true
        text: qsTr("Login")
        enabled: true
        onClicked: rectangle.state = "login"
        background: Rectangle {
            implicitWidth: 100
            implicitHeight: 40
            opacity: enabled ? 1 : 0.3
            color: blueColor
            border.color: borderColor
            border.width: 1
            radius: 8
        }
    }

    Button {
        id: selectCreateUserButton
        x: 450 - (width / 2)
        y: 450
        visible: true
        text: qsTr("Create account")
        enabled: true
        onClicked: rectangle.state = "emailCodeRequest"
        background: Rectangle {
            implicitWidth: 100
            implicitHeight: 40
            opacity: enabled ? 1 : 0.3
            color: greenColor
            border.color: borderColor
            border.width: 1
            radius: 8
        }
    }

    TextField {
        id: emailEdit
        x: 325
        y: 325
        width: 310
        height: 30
        opacity: 0
        visible: true
        wrapMode: Text.Wrap
        placeholderTextColor: placeHolderTextColor
        placeholderText: qsTr("Email")
        enabled: false
        background: Rectangle {
            opacity: enabled ? 1 : 0.3
            color: "#888e95"
            radius: 2
            border.color: borderColor
            border.width: 1
            implicitWidth: parent.width
            implicitHeight: parent.height
        }
    }

    Text {
        id: emailLabel
        x: 250 - (width / 2)
        y: 325
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
        x: 350 - (width / 2)
        y: 450
        opacity: 0
        text: qsTr("Request code")
        onClicked: rectangle.state = "enterEmailVerificationCode"
        background: Rectangle {
            opacity: enabled ? 1 : 0.3
            color: blueColor
            radius: 8
            border.color: borderColor
            border.width: 1
            implicitWidth: 100
            implicitHeight: 40
        }
    }

    TextField {
        id: verificationCodeEdit
        x: 425 - (width / 2)
        y: 325
        width: 175
        height: 30
        opacity: 0
        placeholderTextColor: placeHolderTextColor
        placeholderText: qsTr("Code")
        enabled: false
        background: Rectangle {
            opacity: enabled ? 1 : 0.3
            color: "#888e95"
            radius: 2
            border.color: borderColor
            border.width: 1
            implicitWidth: 250
            implicitHeight: 30
        }
    }

    Text {
        id: verificationCodeLabel
        x: 350 - (width / 2)
        y: 275
        width: 300
        height: 35
        opacity: 0
        color: "#ffffff"
        text: qsTr("A verification code was sent to your email")
        font.pixelSize: 14
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
        enabled: false
    }

    Button {
        id: submitVerificationCode
        x: 450 - (width / 2)
        y: 450
        opacity: 0
        visible: true
        text: qsTr("Submit")
        onClicked: rectangle.state = "createUser"
        background: Rectangle {
            opacity: enabled ? 1 : 0.3
            color: greenColor
            radius: 8
            border.color: borderColor
            border.width: 1
            implicitWidth: 100
            implicitHeight: 40
        }
    }

    Button {
        id: requestNewCodeButton
        x: 250 - (width / 2)
        y: 450
        opacity: 0
        visible: true
        text: qsTr("Request new code")
        background: Rectangle {
            opacity: enabled ? 1 : 0.3
            color: "#deb605"
            radius: 8
            border.color: borderColor
            border.width: 1
            implicitWidth: 100
            implicitHeight: 40
        }
    }

    Button {
        id: createAccountButton
        x: 350 - (width / 2)
        y: 450
        opacity: 0
        text: qsTr("Create account")
        background: Rectangle {
            opacity: enabled ? 1 : 0.3
            color: blueColor
            radius: 8
            border.color: borderColor
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
        x: 60
        y: 260
        opacity: 0
        onClicked: rectangle.state = "initial"
        text: qsTr("Back")
        enabled: false
    }

    Text {
        id: verificationCodeLabel1
        x: 250 - (width / 2)
        y: 325
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
            PropertyChanges {
                target: submitEmailButton
                enabled: false
                opacity: 0
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
