import QtQuick
import QtQuick.Controls

Window {
    id: window
    width: 1920
    height: 1080
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
