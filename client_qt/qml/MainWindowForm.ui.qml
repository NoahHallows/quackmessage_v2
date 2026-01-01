

/*
This is a UI file (.ui.qml) that is intended to be edited in Qt Design Studio only.
It is supposed to be strictly declarative and only uses a subset of QML. If you edit
this file manually, you might introduce QML code that is not supported by Qt Design Studio.
Check out https://doc.qt.io/qtcreator/creator-quick-ui-forms.html for details on .ui.qml files.
*/
import QtQuick
import QtQuick.Controls

Rectangle {
    id: rectangle
    width: 700
    height: 700
    color: "#272727"
    //border.color: "#ff0000"

    property alias sendMessageBtn: sendMessageButton
    property alias messageEdit: messageEdit
    property alias messageList: messageList
    property alias contactsList: contactsList
    property alias yourName: yourContact

    Button {
        id: sendMessageButton
        x: parent.width - 60
        y: parent.height - 60
        text: qsTr("➤")
        icon.color: "#ff0000"
        background: Rectangle {
            implicitWidth: 10
            implicitHeight: 30
            opacity: enabled ? 1 : 0.3
            color: "#00650c"
            border.color: "#21be2b"
            border.width: 1
            radius: 10
        }
    }

    TextField {
        id: messageEdit
        x: parent.width - (parent.width * (50/70))
        y: parent.height - 60
        width: parent.width - (parent.width * (0.3928571428))
        height: 31
        color: "#ffffff"
        wrapMode: Text.Wrap
        placeholderText: qsTr("Message")
        background: Rectangle {
            implicitWidth: parent.width
            implicitHeight: parent.height
            opacity: enabled ? 1 : 0.3
            color: "#888e95"
            border.color: "#21be2b"
            border.width: 1
            radius: 8
        }
    }
    ListView {
        id: messageList
        x: parent.width - (parent.width * (51 / 70))
        y: 8
        width: parent.width * (51 / 70) - 8
        height: parent.height - 100
        boundsBehavior: Flickable.StopAtBounds
        snapMode: ListView.SnapToItem
        clip: true
        spacing: 8
        verticalLayoutDirection: ListView.BottomToTop
        ScrollBar.vertical: ScrollBar {
            policy: ScrollBar.AsNeeded
        }
        model: ListModel {}

        delegate: Item {
            width: messageList.width // Gives MessageBox a parent width to anchor to
            height: msgBox.height
            MessageBox {
                id: msgBox
                messageText: model.messageText
                senderText: model.senderText
                isOwnMessage: model.isOwnMessage
                message_id: model.message_id
                timeText: model.timeText
                timeStamp: model.timeStamp
                seenText: model.seenText
            }
        }

        add: Transition {
            NumberAnimation {
                property: "opacity"
                from: 0
                to: 1.0
                duration: 400
            }
            NumberAnimation {
                property: "scale"
                from: 0
                to: 1.0
                duration: 400
            }
        }

        displaced: Transition {
            NumberAnimation {
                properties: "x,y"
                duration: 400
                easing.type: Easing.OutBounce
            }
        }
    }

    ListView {
        id: contactsList
        x: 8
        y: 8
        width: parent.width * (17 / 70)
        height: parent.width - 100
        spacing: 8
        focus: true
        clip: true
        highlightFollowsCurrentItem: true
        highlight: Rectangle {
            color: "#22ffffff" // Semi-transparent white
            radius: 10
            z: 1
        }
        verticalLayoutDirection: ListView.TopToBottom
        model: ListModel {}
        delegate: ContactElement {
            name: model.name
            messageNum: model.messageNum

            MouseArea {
                anchors.fill: parent

                onClicked: {
                    contactsList.currentIndex = index // Updates the visual selection
                    // We call the function via the backend object
                    messageList.model.clear()
                    backend.set_active_contact(model.name)
                    contactsList.model.setProperty(index, "messageNum", "0")
                }
            }
        }
        add: Transition {
            NumberAnimation {
                property: "opacity"
                from: 0
                to: 1.0
                duration: 400
            }
            NumberAnimation {
                property: "scale"
                from: 0
                to: 1.0
                duration: 400
            }
        }

        displaced: Transition {
            NumberAnimation {
                properties: "x,y"
                duration: 400
                easing.type: Easing.OutBounce
            }
        }
    }

    ContactElement {
        id: yourContact
        x: 8
        y: parent.height - 60
        color: "#b261ff"
    }
}
