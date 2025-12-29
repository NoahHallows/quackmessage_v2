import QtQuick
import QtQuick.Controls

Rectangle {
    id: root
    width: 100
    height: 30
    radius: 10
    //color: "lightsteelblue"

    property alias name: contactName.text

    //border.color: ListView.isCurrentItem ? "#21be2b" : "transparent"
    //border.width: ListView.isCurrentItem ? 2 : 0

    // You can also change the background color slightly
    color: ListView.isCurrentItem ? "#444444" : "#333333"

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
}
