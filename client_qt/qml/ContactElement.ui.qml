import QtQuick
import QtQuick.Controls

Rectangle {
    id: root
    width: 100
    height: 30
    radius: 10

    property alias name: contactName.text
    property alias messageNum: messageNum.text


    // You can also change the background color slightly
    color: "#444444"

    Text {
        id: contactName
        x: 8
        y: 8
        color: "#000000"
        width: parent.width - 16
        wrapMode: Text.WordWrap
        text: qsTr("Name")
        font.pixelSize: 12
    }

    RoundButton {
        id: messageNum
        x: 67
        y: 3
        width: 25
        height: 25
        contentItem: Text {
            text: messageNum.text
            font.pixelSize: 14
            // This will shrink the font until the text fits the width of the button
            fontSizeMode: Text.Fit
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            color: "white"
        }
        visible: text !== "0" && text !== ""

        font.pixelSize: {
            if (text.length <= 2) return 12;
            if (text.length === 3) return 10;
            return 8; // Smallest size for 4+ digits
        }
        background: Rectangle {
            radius: parent.width / 2
            color: "#ff4444" // Red notification bubble
        }
    }
}
