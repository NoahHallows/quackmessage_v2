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
    width: 1920
    height: 1080

    Button {
        id: sendMessageButton;
        x: 979
        y: 712
        text: qsTr("Send")
        background: Rectangle {
            implicitWidth: 145
            implicitHeight: 31
            opacity: enabled ? 1 : 0.3
            color: "#00650c"
            border.color: "#21be2b"
            border.width: 1
            radius: 2
        }
    }
    TextField {
        id: senderEdit;
        x: 979
        y: 516
        width: 145
        height: 31
        opacity: 1
        enabled: true
        placeholderText: qsTr("Sender")
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
    TextField {
        id: receiverEdit;
        x: 979
        y: 460
        width: 145
        height: 31
        opacity: 1
        enabled: true
        placeholderText: qsTr("Receiver")
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

    TextArea {
        id: messageEdit
        x: 979
        y: 585
        placeholderText: qsTr("Message")
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

    ListView {
        id: listView
        x: 668
        y: 638
        width: 160
        height: 80
        orientation: ListView.Vertical
        verticalLayoutDirection: ListView.BottomToTop
        model: ListModel {
            ListElement {
                name: "Red"
                colorCode: "red"
            }

            ListElement {
                name: "Green"
                colorCode: "green"
            }

            ListElement {
                name: "Blue"
                colorCode: "blue"
            }

            ListElement {
                name: "White"
                colorCode: "white"
            }
        }
        delegate: Row {
            spacing: 5
            Rectangle {
                width: 100
                height: 10
                color: colorCode
            }

            Text {
                width: 100
                text: name
            }
        }
    }
    ListView {
        width: 240; height: 320
        model: ListModel {}

        delegate: Rectangle {
            width: 100; height: 30
            border.width: 1
            color: "lightsteelblue"
            Text {
                anchors.centerIn: parent
                text: name
            }
        }

        add: Transition {
            NumberAnimation { property: "opacity"; from: 0; to: 1.0; duration: 400 }
            NumberAnimation { property: "scale"; from: 0; to: 1.0; duration: 400 }
        }

        displaced: Transition {
            NumberAnimation { properties: "x,y"; duration: 400; easing.type: Easing.OutBounce }
        }

        //focus: true
        //Keys.onSpacePressed: model.insert(0, { "name": "Item " + model.count })
    }
}
