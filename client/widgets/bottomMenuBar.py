# MenuBar (Logo, ServerInfo, Login/Logout) Top menu of UI
import pygame
from guizero import Box, Text, PushButton, Picture, TextBox, event

from client.widgets.loginWindow import LoginWindow
import globals


class BottomMenuBar:
    def __init__(self, parent, messenger, chatcontent):

        def handle_submit_button():
            if self.textInput.value != "":
                print(self.textInput.value)
                Text(chatcontent, text=self.textInput.value)
                messenger.send_message(self.textInput.value)

        self.container = Box(parent)
        self.container.width = "fill"
        self.container.align = "bottom"
        self.container.border = False
        self.container.height = 50
        self.container.bg = "#40466F"

        self.chatBox = Box(self.container, align="bottom", width="fill", height=30)
        self.chatBox.bg = "#40466F"

        self.textInput = TextBox(self.chatBox, align="left", width="fill", height= 30)
        self.textInput.bg = "dimgrey"
        self.textInput.text_color = "#BCDAE6"
        self.textInput.tk.config(highlightthickness=0, relief="groove")
        self.sendText = PushButton(self.chatBox, align="right", width=70, image="images/send.png", command=handle_submit_button )

