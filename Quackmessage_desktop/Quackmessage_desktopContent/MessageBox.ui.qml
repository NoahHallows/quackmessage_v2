

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
    width: 150
    height: 100
    radius: 10

    Text {
        id: text1
        x: 8
        y: 8
        width: 134
        height: 63
        text: qsTr("Message: ")
        font.pixelSize: 12
    }

    Text {
        id: text2
        x: 8
        y: 77
        width: 99
        height: 15
        text: qsTr("Sent by: ")
        font.pixelSize: 12
    }
}
