import QtQuick
import QtQuick.Controls

Rectangle {
    id: mainScreen
    anchors.fill: parent
    visible: true

    MainWindowForm {
        id: mainUI
        anchors.fill: parent
        sendMessageBtn.onClicked: {
            if (messageEdit.text.length > 0) {
                backend.send_message(messageEdit.text)
                messageEdit.clear()
            }
        }

        messageEdit.onAccepted: {
            if (messageEdit.text.length > 0) {
                backend.send_message(messageEdit.text)
                messageEdit.clear()
            }
        }



        function showMessage(sender, message, message_id, time_string, time_stamp) {
            if (sender === "You") {
                var isOwnMessage = true
            }
            else {
                var isOwnMessage = false
            }
            messageList.model.insert(0, { "messageText": message , "senderText":
            "Sent by: " + sender, "isOwnMessage": isOwnMessage, "message_id":
            message_id, "timeText": time_string, "timeStamp": time_stamp,
            "seenText": ""})
        }

        function newMessageDeactive(sender) {
            for (var i = 0; i < mainUI.contactsList.model.count; i++) {
                var contact = mainUI.contactsList.model.get(i);
                if (contact.name === sender) {
                    // Increment the current count
                    var currentCount = parseInt(contact.messageNum);
                    mainUI.contactsList.model.setProperty(i, "messageNum", (currentCount + 1).toString());
                    break;
                }
            }
        }

        function updateMessageSeen(message_id, time_string, time_stamp) {
            for (var i = 0; i < mainUI.messageList.model.count; i++) {
                var message = mainUI.messageList.model.get(i);
                if (message.message_id == message_id) {
                    mainUI.contactsList.model.setProperty(i, "seenText", time_string);
                    break;
                }
            }
        }


        function createContact(contactName) {
            contactsList.model.append({"name": contactName, "messageNum": "0"})
        }

        function getRelativeTime(msTimestamp) {
            if (!msTimestamp) return "";

            let now = Date.now();
            let diff = Math.floor((now - msTimestamp) / 1000); // Difference in seconds

            if (diff < 60) return "just now";
            if (diff < 3600) return Math.floor(diff / 60) + "m ago";
            if (diff < 86400) return Math.floor(diff / 3600) + "h ago";

            // For older messages, format as a real date
            let date = new Date(msTimestamp);
            return date.toLocaleDateString(undefined, { month: 'short', day: 'numeric' });
        }

        Connections {
            target: backend
            // New message from selected user
            function onNewMessageActive(sender, message, message_id, time_sent_ms) {
                mainUI.showMessage(sender, message, message_id,
                mainUI.getRelativeTime(time_sent_ms), time_sent_ms)
            }
            // New message for non selected user
            function onNewMessageDeactive(sender) {
                console.log("EIOGHOUGH")
                mainUI.newMessageDeactive(sender)
            }

            function onAddContactSignal(name) {
                mainUI.createContact(name)
            }
            function onSetUserName(name) {
                mainUI.yourName.name = "You are " + name
            }
            function onMessageSeen(message_id, timestamp) {
                mainUI.updateMessageSeen(message_id, mainUI.getRelativeTime(timestamp))
            }
        }

        Timer {
            //interval: 10000
            interval: 30000 // Update every 30 seconds for better accuracy
            running: true
            repeat: true
            onTriggered: {
                for (var i = 0; i < mainUI.messageList.model.count; i++) {
                    let item = mainUI.messageList.model.get(i);
                    if (item.timeStamp) {
                        let updatedTime = mainUI.getRelativeTime(item.timeStamp);
                        // Only update if the string actually changed to save performance
                        if (item.timeStr !== updatedTime) {
                            mainUI.messageList.model.setProperty(i, "timeText", updatedTime);
                        }
                    }
                }
            }
        }
    }
}
