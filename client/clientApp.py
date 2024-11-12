# Client Chat Application.
"""
Launch this file to start the chat application.
"""

# Import Libraries
from guizero import App, Text, Box, TextBox, Picture, PushButton, TitleBox
from login import open_login
import pygame as pygame

# Sound initializations
pygame.mixer.init()
connected = pygame.mixer.Sound("sounds/connected.wav")
disconnected = pygame.mixer.Sound("sounds/disconnected.wav")


# clientApp.py Functions

# handles retrieving login information from the login window. Currently, in a test and will just resolve the name of
# the server
def handle_returned_login(value):
    serverInfo.value = f"Connected To: {value}"
    loginButton.image = "images/logout.png"
    loginButton.width = 80
    loginButton.tk.config(borderwidth=0, highlightthickness=0)
    loginButton.update_command(command=logout)
    connected.set_volume(.1)
    connected.play()


# logs the user out of the server. This will send a request to delete the sessionID from the server for the user.
# Currently, has no effect
def logout():
    loginButton.image = "images/login.png"
    loginButton.width = 80
    loginButton.tk.config(borderwidth=0, highlightthickness=0)
    loginButton.update_command(command=open_login, args=[app, handle_returned_login])
    serverInfo.value = "Not Connected to a Server."
    disconnected.set_volume(.1)
    disconnected.play()


# Application UI Initialization
app = App(width=700, height=600, bg="dimgrey")
app.tk.minsize(600, 500)

# MenuBar (Logo, ServerInfo, Login/Logout) Top menu of UI
menuBar = Box(app, width="fill", align="top", border=False, height=40)
menuBar.tk.configure(background="#40466F")
confabLogo = Picture(menuBar, image="images/confabTransparent.png", align='left', height=40, width=200)
confabLogo.tk.configure(background="#40466F")
serverInfo = Text(menuBar, text="Not Connected to a Server.", align="left", bg="#40466F", color="#BCDAE6")
login_image = "images/login.png"
loginButton = PushButton(menuBar, image="images/login.png", command=open_login, args=[app, handle_returned_login],
                         align="right", width=90)
loginButton.tk.config(borderwidth=0, highlightthickness=0)

# Bottom Text Bar (Empty Box, ChatBox, Send Button) Bottom menu of UI
bottom_box = Box(app, width="fill", align="bottom", border=False, height=40)
bottom_box.bg = "#40466F"
Box(bottom_box, align='left', width=200, height=40)
chatBox = Box(bottom_box, align="bottom", width="fill", height=40)
chatBox.bg = "#40466F"
textInput = TextBox(chatBox, align="left", width="fill", height="fill")
textInput.bg = "dimgrey"
textInput.text_color = "#BCDAE6"
textInput.tk.config(highlightthickness=0, relief="groove")
sendText = PushButton(chatBox, align="right", width=70, image="images/send.png")

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

# Displays the Application UI
app.display()
