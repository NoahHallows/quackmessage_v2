import QtQuick
import QtQuick.Controls

Rectangle {
    id: root
    width: 100
    height: 30
    radius: 10
    color: "lightsteelblue"

    property alias name: contactName.text

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
