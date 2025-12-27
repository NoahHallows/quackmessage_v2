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
            showMessage("You", messageEdit.text)
        }

        function showMessage(sender, message) {
            console.log(message)
            if (sender === "You") {
                var box_color = "#5e0549"
            }
            else {
                var box_color = "#c754bb"
            }
            messageList.model.insert(0, { "messageText": message , "senderText":
            "Sent by: " + sender, "messageColor": box_color})
        }

        Connections {
            target: backend
            function onNewMessage(sender, message) {
                mainUI.showMessage(sender, message)
            }
        }
    }
}
