import QtQuick
import QtQuick.Controls

Rectangle {
    id: mainScreen
    width: 1920
    height: 1080
    visible: true

    MainWindowForm {
        sendMessageBtn.onClicked: {
            console.log("Send button clicked")
            backend.send_message(receiverEdit.text, messageEdit.text)
        }
    }
}
