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



        function showMessage(sender, message, message_id, time_string,
        time_stamp, time_seen_ms) {
            if (sender === "You") {
                var isOwnMessage = true
                if (time_seen_ms != -36000000) {
                    var seen_text = mainUI.getRelativeTime(time_seen_ms)
                    if (mainUI.messageList.model.count > 0) {
                        mainUI.messageList.model.get(0).seenText = ""
                    }
                }
                else {
                    var seen_text = ""
                }
            }
            else {
                var isOwnMessage = false
                var seen_text = ""
            }
            messageList.model.insert(0, { "messageText": message , "senderText":
            "Sent by: " + sender, "isOwnMessage": isOwnMessage, "message_id":
            message_id, "timeText": time_string, "timeStamp": time_stamp,
            "seenText": seen_text, "time_seen_ms": time_seen_ms})
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
            console.log("Updating seen status")
            for (var i = 0; i < mainUI.messageList.model.count; i++) {
                var message = mainUI.messageList.model.get(i);
                mainUI.messageList.model.setProperty(i, "seenText", "");
                if (message.message_id == message_id) {
                    console.log("Match found")
                    console.log(time_string)
                    mainUI.messageList.model.setProperty(i, "seenText", time_string);
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
            function onNewMessageActive(sender, message, message_id, time_sent_ms, seen_time_ms) {
                mainUI.showMessage(sender, message, message_id,
                mainUI.getRelativeTime(time_sent_ms), time_sent_ms,
                seen_time_ms)
            }
            // New message for non selected user
            function onNewMessageDeactive(sender) {
                mainUI.newMessageDeactive(sender)
            }

            function onAddContactSignal(name) {
                mainUI.createContact(name)
            }
            function onSetUserName(name) {
                mainUI.yourName.name = "You are " + name
            }
            function onMessageSeen(message_id, timestamp) {
                console.log(message_id + " has been seen")
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
                        let updatedTimeSent = mainUI.getRelativeTime(item.timeStamp);
                        let updatedTimeSeen = mainUI.getRelativeTime(item.time_seen_ms)
                        // Only update if the string actually changed to save performance
                        if (item.timeText !== updatedTimeSent) {
                            mainUI.messageList.model.setProperty(i, "timeText",
                            updatedTimeSent);
                        }
                        if (item.seenText !== updatedTimeSeen && item.seenText !== "") {
                            mainUI.messageList.model.setProperty(i, seenText,
                            updatedTimeSeen)
                        }
                    }
                }
            }
        }
    }
}
