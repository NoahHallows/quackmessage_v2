import QtQuick
import QtQuick.Controls

Window {
    id: window
    width: 500
    height: 700
    visible: true
    title: "Quackmessage"

    Loader {
        id: mainLoader
        anchors.fill: parent
        source: "Login.qml"
    }

    function showMainWindow() {
        mainLoader.source = "MainWindow.qml"
    }

    Connections {
        target: backend
        function onLoginSuccess() {
            showMainWindow()
        }
    }
}
