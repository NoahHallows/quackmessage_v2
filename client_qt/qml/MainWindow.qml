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
            backend.send_message(messageEdit.text)
            showMessage("You", messageEdit.text)
            messageEdit.clear()
        }


        function showMessage(sender, message) {
            if (sender === "You") {
                var box_color = "#5e0549"
            }
            else {
                var box_color = "#c754bb"
            }
            messageList.model.insert(0, { "messageText": message , "senderText":
            "Sent by: " + sender, "messageColor": box_color})
        }

        function createContact(contactName) {
            contactsList.model.append({"name": contactName})
        }

        Connections {
            target: backend
            function onNewMessage(sender, message, message_id) {
                mainUI.showMessage(sender, message)
            }
            function onAddContactSignal(name) {
                mainUI.createContact(name)
            }
        }
    }
}
