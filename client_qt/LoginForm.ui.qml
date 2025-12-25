/*
This is a UI file (.ui.qml) that is intended to be edited in Qt Design Studio only.
It is supposed to be strictly declarative and only uses a subset of QML. If you edit
this file manually, you might introduce QML code that is not supported by Qt Design Studio.
Check out https://doc.qt.io/qtcreator/creator-quick-ui-forms.html for details on .ui.qml files.
*/

import QtQuick
import QtQuick.Controls
//import Quackmessage_desktop
//import QtQuick.Studio.DesignEffects

Rectangle {
    id: rectangle
    width: 1920
    height: 1080
    state: "initial"
    color: "#ffffff"

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

    Text {
        id: title;
        x: 823
        y: 328
        width: 275
        height: 136
        text: qsTr("Quackmessage\nLogin")
        font.pixelSize: 30
        horizontalAlignment: Text.AlignHCenter
    }

/*    Image {
        id: logo;
        x: 910
        y: 222
        width: 100
        height: 100
        source: "qrcimages/template_image.png"
        fillMode: Image.PreserveAspectFit
    }*/

    Text {
        id: userNameLabel;
        x: 854
        y: 530
        width: 90
        height: 36
        opacity: 0
        text: qsTr("Username")
        font.pixelSize: 14
        enabled: false
    }

    TextField {
        id: usernameEdit;
        x: 986
        y: 525
        width: 145
        height: 31
        opacity: 0
        enabled: false
        placeholderText: qsTr("Username")
        background: Rectangle {
            implicitWidth: 145
            implicitHeight: 31
            opacity: enabled ? 1 : 0.3
            color: "#888e95"
            border.color: "#21be2b"
            border.width: 1
            radius: 2
        }
    }

    Text {
        id: passwordLabel;
        x: 854
        y: 606
        width: 90
        height: 36
        opacity: 0
        text: qsTr("Password")
        font.pixelSize: 14
        enabled: false
    }

    TextField {
        id: passwordEdit;
        x: 986
        y: 601
        width: 145
        height: 31
        opacity: 0
        echoMode: TextInput.Password
        enabled: false
        placeholderText: qsTr("Password")
        background: Rectangle {
            implicitWidth: 145
            implicitHeight: 31
            opacity: enabled ? 1 : 0.3
            color: "#888e95"
            border.color: "#21be2b"
            border.width: 1
            radius: 2
        }
    }

    Button {
        id: loginButton;
        x: 910
        y: 698
        opacity: 0
        text: qsTr("Login")
        enabled: usernameEdit.text.length > 0 && passwordEdit.text.length > 0
        onClicked: console.log("Here")
        background: Rectangle {
            implicitWidth: 100
            implicitHeight: 40
            opacity: enabled ? 1 : 0.3
            color: "#0072ff"
            border.color: "#21be2b"
            border.width: 1
            radius: 2
        }
    }

    Button {
        id: selectLoginButton
        x: 823
        y: 484
        visible: true
        text: qsTr("Login")
        enabled: true
        onClicked: rectangle.state = "login"
        background: Rectangle {
            implicitWidth: 100
            implicitHeight: 40
            opacity: enabled ? 1 : 0.3
            color: "#0072ff"
            border.color: "#21be2b"
            border.width: 1
            radius: 2
        }
    }

    Button {
        id: selectCreateUserButton
        x: 986
        y: 484
        visible: true
        text: qsTr("Create account")
        enabled: true
        onClicked: rectangle.state = "emailCodeRequest"
        background: Rectangle {
            implicitWidth: 100
            implicitHeight: 40
            opacity: enabled ? 1 : 0.3
            color: "#007429"
            border.color: "#21be2b"
            border.width: 1
            radius: 2
        }
    }

    TextField {
        id: emailEdit
        x: 986
        y: 525
        width: 253
        height: 31
        opacity: 0
        visible: true
        placeholderText: qsTr("Email")
        enabled: false
        background: Rectangle {
            opacity: enabled ? 1 : 0.3
            color: "#888e95"
            radius: 2
            border.color: "#21be2b"
            border.width: 1
            implicitWidth: 253
            implicitHeight: 31
        }
    }

    Text {
        id: emailLabel
        x: 854
        y: 530
        width: 106
        height: 36
        opacity: 0
        text: qsTr("Enter your email:")
        font.pixelSize: 14
        enabled: false
    }

    Button {
        id: submitEmailButton
        x: 910
        y: 572
        opacity: 0
        visible: true
        text: qsTr("Request code")
        enabled: emailEdit.text.length > 0
        onClicked: rectangle.state = "enterEmailVerificationCode"
        background: Rectangle {
            opacity: enabled ? 1 : 0.3
            color: "#0d60a9"
            radius: 2
            border.color: "#21be2b"
            border.width: 1
            implicitWidth: 100
            implicitHeight: 40
        }
    }

    TextField {
        id: verificationCodeEdit
        x: 986
        y: 525
        width: 253
        height: 31
        opacity: 0
        visible: true
        placeholderText: qsTr("Code")
        enabled: false
        background: Rectangle {
            opacity: enabled ? 1 : 0.3
            color: "#888e95"
            radius: 2
            border.color: "#21be2b"
            border.width: 1
            implicitWidth: 253
            implicitHeight: 31
        }
    }

    Text {
        id: verificationCodeLabel
        x: 683
        y: 530
        width: 277
        height: 36
        opacity: 0
        text: qsTr("Enter the code we just sent to your email")
        font.pixelSize: 14
        enabled: false
    }

    Button {
        id: submitVerificationCode
        x: 986
        y: 597
        opacity: 0
        visible: true
        text: qsTr("Submit")
        enabled: verificationCodeEdit.text.length > 0
        onClicked: rectangle.state = "createUser"
        background: Rectangle {
            opacity: enabled ? 1 : 0.3
            color: "#0da91f"
            radius: 2
            border.color: "#21be2b"
            border.width: 1
            implicitWidth: 100
            implicitHeight: 40
        }
    }

    Button {
        id: requestNewCodeButton
        x: 782
        y: 597
        opacity: 0
        visible: true
        text: qsTr("Request new code")
        enabled: false
        background: Rectangle {
            opacity: enabled ? 1 : 0.3
            color: "#deb605"
            radius: 2
            border.color: "#21be2b"
            border.width: 1
            implicitWidth: 100
            implicitHeight: 40
        }
    }

    Button {
        id: createAccountButton
        x: 910
        y: 698
        opacity: 0
        text: qsTr("Create account")
        enabled: usernameEdit.text.length > 0 && passwordEdit.text.length > 0
        background: Rectangle {
            opacity: enabled ? 1 : 0.3
            color: "#0072ff"
            radius: 2
            border.color: "#21be2b"
            border.width: 1
            implicitWidth: 100
            implicitHeight: 40
        }
    }

    states: [
        State {
            name: "initial"
        },

        State {
            name: "login"
            PropertyChanges {target: userNameLabel; enabled: true; opacity: 1; scale: 1.0}
            PropertyChanges {target: usernameEdit; enabled: true; opacity: 1; scale: 1.0}
            PropertyChanges {target: passwordEdit; enabled: true; opacity: 1; scale: 1.0}
            PropertyChanges {target: passwordLabel; enabled: true; opacity: 1; scale: 1.0}
            PropertyChanges {target: loginButton; enabled: true; opacity: 1; scale: 1.0}
            PropertyChanges {target: selectCreateUserButton; enabled: false; opacity: 0; scale: 1.0}
            PropertyChanges {target: selectLoginButton; enabled: false; opacity: 0; scale: 1.0}
        },

        State {
            name: "createUser"
            PropertyChanges {target: userNameLabel; enabled: true; opacity: 1; scale: 1.0}
            PropertyChanges {target: usernameEdit; enabled: true; opacity: 1; scale: 1.0}
            PropertyChanges {target: passwordEdit; enabled: true; opacity: 1; scale: 1.0}
            PropertyChanges {target: passwordLabel; enabled: true; opacity: 1; scale: 1.0}
            PropertyChanges {target: verificationCodeEdit; enabled: false; opacity: 0; scale: 1.0}
            PropertyChanges {target: verificationCodeLabel; enabled: false; opacity: 0; scale: 1.0}
            PropertyChanges {target: submitVerificationCode; enabled: false; opacity: 0; scale: 1.0}
            PropertyChanges {target: requestNewCode; enabled: false; opacity: 0; scale: 1.0}
            PropertyChanges {target: selectCreateUserButton; enabled: false; opacity: 0; scale: 1.0}
            PropertyChanges {target: selectLoginButton; enabled: false; opacity: 0; scale: 1.0}


        },

        State {
            name: "emailCodeRequest"
            PropertyChanges {target: emailLabel; enabled: true; opacity: 1; scale: 1.0}
            PropertyChanges {target: emailEdit; enabled: true; opacity: 1; scale: 1.0}
            PropertyChanges {target: submitEmailButton; enabled: true; opacity: 1; scale: 1.0}
            PropertyChanges {target: selectCreateUserButton; enabled: false; opacity: 0; scale: 1.0}
            PropertyChanges {target: selectLoginButton; enabled: false; opacity: 0; scale: 1.0}
        },

        State {
            name: "enterEmailVerificationCode"
            PropertyChanges {target: emailLabel; enabled: false; opacity: 0; scale: 1.0}
            PropertyChanges {target: emailEdit; enabled: false; opacity: 0; scale: 1.0}
            PropertyChanges {target: submitEmailButton; enabled: false; opacity: 0; scale: 1.0}
            PropertyChanges {target: verificationCodeEdit; enabled: true; opacity: 1; scale: 1.0}
            PropertyChanges {target: verificationCodeLabel; enabled: true; opacity: 1; scale: 1.0}
            PropertyChanges {target: submitVerificationCode; enabled: true; opacity: 1; scale: 1.0}
            PropertyChanges {target: requestNewCode; enabled: true; opacity: 1; scale: 1.0}
            PropertyChanges {target: selectCreateUserButton; enabled: false; opacity: 0; scale: 1.0}
            PropertyChanges {target: selectLoginButton; enabled: false; opacity: 0; scale: 1.0}
        }

    ]

    transitions: Transition {
        NumberAnimation { properties: "opacity,scale"; duration: 100; easing.type: Easing.OutCubic }
    }
}
