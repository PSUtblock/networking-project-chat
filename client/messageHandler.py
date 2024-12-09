import globals

from client.widgets.chatMessage import ChatMessage


# Once a text message is recieved this function appends a message container to
# The content box
def message_handler(server_message):
    parts = server_message.split("|")

    if parts[0] == "CHAT_MESSAGE":
        ChatMessage(globals.contentBox, parts[2], parts[3], parts[4])
    else:
        print("Unable to handle message.")
