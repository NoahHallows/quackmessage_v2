import QtQuick
import QtQuick.Controls

// 1. Change the root element to an Item (transparent container)
Item {
    id: root
    width: 320
    // 2. Calculate height dynamically: Bubble height + Label height (only if visible)
    height: bubble.height + (statusLabel.visible ? statusLabel.height + 5 : 0)

    property int message_id: 0
    // Use a double for the bigger range despite me not being a fan of floats
    // for this
    property double timeStamp: 0
    property double time_seen_ms: 0

    // Aliases must now point to the items which are moved inside 'bubble'
    property alias messageText: messageText.text
    property alias senderText: senderText.text
    property alias timeText: timeText.text
    property alias seenText: statusLabel.text // Points to the label below the bubble

    property bool isOwnMessage: false

    // Move layout anchors here (left/right alignment)
    anchors.right: isOwnMessage ? parent.right : undefined
    anchors.left: isOwnMessage ? undefined : parent.left


    // 3. Move the colored background into this inner Rectangle ('bubble')
    Rectangle {
        id: bubble
        width: parent.width
        // Height calculation remains based on the text inside
        height: messageText.implicitHeight + senderText.implicitHeight + 24
        radius: 10


        // Move the color logic here
        color: isOwnMessage ? "#b261ff" : "#539fe4"

        // 4. Keep the message content inside the bubble
        Text {
            id: messageText
            anchors.top: parent.top
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.margins: 8
            wrapMode: Text.Wrap
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
    }

    // 5. Position the status label BELOW the bubble
    Text {
        id: statusLabel
        anchors.top: bubble.bottom
        anchors.right: parent.right
        anchors.topMargin: 5 // Add a little spacing

        // 6. Logic to hide it completely if empty
        visible: text !== ""

        text: "" // Default is empty so it takes no space
        font.pixelSize: 10
        color: "gray"
    }
}
