

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

    property int message_id: 0
    property int timeStamp: 0

    property alias messageText: messageText.text
    property alias senderText: senderText.text
    property alias timeText: timeText.text
    property alias seenText: statusLabel.text

    property bool isOwnMessage: false

    anchors.left: isOwnMessage ? undefined : parent.left
    anchors.right: isOwnMessage ? parent.right : undefined

    // Change color based on who sent it
    // first if you sent it, second not you
    color: isOwnMessage ?  "#b261ff" : "#539fe4"
    Column {
        id: messageColumn
        anchors.top: parent.top
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.margins: 12 // Uniform margins for the column
        spacing: 4

        Text {
            id: messageText
            anchors.top: parent.top
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.margins: 8
            wrapMode: Text.WordWrap
            text: qsTr("Message: ")
            font.pixelSize: 12
        }

        Text {
            id: senderText
            anchors.top: messageText.bottom
            anchors.margins: 8
            anchors.right: parent.right
            x: 8
            width: parent.width - 16
            text: qsTr("Sent by: ")
            font.pixelSize: 10
            font.italic: true
        }
        Text {
            id: timeText
            anchors.bottom: parent.bottom
            anchors.right: parent.right
            anchors.margins: 8
            x: parent.width - 20
            y: parent.height - 15
            text: qsTr("Text")
            font.pixelSize: 8
        }

        Text {
            id: statusLabel
            text: model.statusText || "" // Use the property from the model
            visible: text !== ""
            font.pixelSize: 10
            color: "#aaaaaa"
            anchors.right: isOwnMessage ? parent.right : undefined
            anchors.left: !isOwnMessage ? parent.left : undefined
        }
    }
}
