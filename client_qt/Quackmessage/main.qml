import QtQuick
import QtQuick.Controls

Window {
    width: 640
    height: 480
    visible: true
    title: "Arch Linux PySide6 App"

    Rectangle {
        anchors.fill: parent
        color: "#1793d1" // Arch Linux Blue

        Text {
            anchors.centerIn: parent
            text: "Hello from QML on Arch!"
            color: "white"
            font.pixelSize: 24
        }
    }
}
