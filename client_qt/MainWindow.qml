import QtQuick
import QtQuick.Controls

Rectangle {
    id: mainScreen
    width: 250
    height: 500
    visible: true

    MainWindowForm {
        id: mainUI
        sendMessageBtn.onClicked: {
            console.log("Send button clicked")
            backend.send_message(receiverEdit.text, messageEdit.text)
            showMessage(receiverEdit.text, messageEdit.text)
        }

        function showMessage(sender, message) {
            console.log(message)
            messageList.model.insert(0, { "messageText": message , "senderText": "Sent by: " + sender})
        }

        Connections {
            target: backend
            function onNewMessage(sender, message) {
                mainUI.showMessage(sender, message)
            }
        }
    }
}
