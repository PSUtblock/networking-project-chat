# Client Chat Application.
"""
Launch this file to start the chat application.
"""
from cryptography.fernet import Fernet
# Import Libraries
from guizero import App, Text, Box, TextBox, Picture, PushButton, TitleBox

from client.clientListener import ClientSocketListener
from client.clientListenerFunctions import ClientMessenger
from client.widgets.bottomMenuBar import BottomMenuBar
from client.widgets.chatMessage import ChatMessage
from client.widgets.topMenuBar import TopMenuBar
from login import open_login
import pygame as pygame
import globals

# Sound initializations
pygame.mixer.init()
connected = pygame.mixer.Sound("sounds/connected.wav")

# Client memory
globals.client_username = "Empty"
globals.session_id = None
globals.client_listen = ClientSocketListener("0.0.0.0", "12345")
globals.client_messenger = ClientMessenger("0.0.0.0", "12345", Fernet.generate_key())

# Application UI Initialization
app = App(width=700, height=600, bg="#40466F")
app.tk.minsize(600, 500)

# Class widget that generates the Top Menu UI
TopMenuBar(app)

# Channel and User Group  (channelBox, userBox) Left Column of UI
groupsMenu = Box(app, height="fill", align="left", border=False, width=200)
groupsMenu.bg = "#40466F"
Box(groupsMenu, align="left", height="fill", width=5)
Box(groupsMenu, align="right", height="fill", width=5)
Box(groupsMenu, align="top", height=10, width="fill")

# channelBox is the UI you want to target and populate with Channels
# May need a nested widget to handle scrolling and selection
channelBox = TitleBox(groupsMenu, "Chat Channels", width="fill", height="fill")
channelBox.tk.config(relief="sunken")
Box(groupsMenu, align="top", height=10, width="fill")

# userBox is the UI you want to target and populate with active users
# May need a nested widget to handle scrolling and selection
userBox = TitleBox(groupsMenu, "Active Users", width="fill", height="fill")
userBox.tk.config(relief="sunken")
Box(groupsMenu, align="top", height=10, width="fill")

# contentBox is the main UI window. Chat messages will go within this UI section
# May need to add a nested widget to handle scrolling
contentBox = Box(app, align="top", width="fill", height="fill", border=False)
contentBox.bg = 'dimgrey'
message1 = ChatMessage(contentBox, "nothing", "nothing")

# Bottom Text Bar (Empty Box, ChatBox, Send Button) Bottom menu of UI
BottomMenuBar(app, globals.client_messenger, contentBox)

# Displays the Application UI
app.display()
app.focus()
