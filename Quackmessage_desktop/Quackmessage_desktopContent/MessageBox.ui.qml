

/*
This is a UI file (.ui.qml) that is intended to be edited in Qt Design Studio only.
It is supposed to be strictly declarative and only uses a subset of QML. If you edit
this file manually, you might introduce QML code that is not supported by Qt Design Studio.
Check out https://doc.qt.io/qtcreator/creator-quick-ui-forms.html for details on .ui.qml files.
*/
import QtQuick
import QtQuick.Controls

Rectangle {
    id: root
    width: 320
    height: messageText.implicitHeight + senderText.implicitHeight + 24
    radius: 10
    color: "lightsteelblue"

    property alias messageText: messageText.text
    property alias senderText: senderText.text
    property alias messageColor: root.color

    Text {
        id: messageText
        x: 8
        y: 8
        width: parent.width - 16
        wrapMode: Text.WordWrap
        text: qsTr("Message: ")
        font.pixelSize: 12
    }

    Text {
        id: senderText
        anchors.top: messageText.bottom
        anchors.topMargin: 4
        x: 8
        width: parent.width - 16
        text: qsTr("Sent by: ")
        font.pixelSize: 10
        font.italic: true
    }
    Text {
        id: receiptText
        x: parent.width - 20
        y: parent.height - 8
        text: qsTr("Text")
        font.pixelSize: 8
    }
}
