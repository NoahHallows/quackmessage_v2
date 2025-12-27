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
            //showMessage("You", messageEdit.text)
            messageEdit.clear()
        }


        function showMessage(sender, message, message_id) {
            if (sender === "You") {
                var isOwnMessage = true
            }
            else {
                var isOwnMessage = false
            }
            messageList.model.insert(0, { "messageText": message , "senderText":
            "Sent by: " + sender, "isOwnMessage": isOwnMessage, "message_id":
            message_id})
        }

        function createContact(contactName) {
            contactsList.model.append({"name": contactName})
        }

        Connections {
            target: backend
            function onNewMessage(sender, message, message_id) {
                mainUI.showMessage(sender, message, message_id)
            }
            function onAddContactSignal(name) {
                mainUI.createContact(name)
            }
        }
    }
}
