import QtQuick
import Quackmessage_desktop

Window {
    width: mainScreen.width
    height: mainScreen.height

    visible: true
    title: "Quackmessage_desktop"

    Login {
        id: mainScreen

        anchors.centerIn: parent
    }

}

