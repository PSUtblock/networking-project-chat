# MenuBar (Logo, ServerInfo, Login/Logout) Top menu of UI
import pygame
from guizero import Box, Text, PushButton, Picture

from client.widgets.loginWindow import LoginWindow


class TopMenuBar:
    def __init__(self, parent):

        self.container = Box(parent)
        self.container.width = "fill"
        self.container.align = "top"
        self.container.border = False
        self.container.height = 40
        self.container.tk.configure(background="#40466F")

        self.logo = Picture(self.container, image="images/confabTransparent.png", align='left', height=40, width=200)
        self.logo.tk.configure(background="#40466F")
        self.server_info = Text(self.container, text="Not Connected to a Server.", align="left", bg="#40466F",
                                color="#BCDAE6")
        self.loginButton = PushButton(self.container, image="images/login.png", command="nothing", width=90,
                                      align="right")
        self.loginButton.tk.config(borderwidth=0, highlightthickness=0)

        pygame.mixer.init()
        self.disconnected = pygame.mixer.Sound("sounds/disconnected.wav")
        self.connected = pygame.mixer.Sound("sounds/connected.wav")

        self.loginMenu = LoginWindow(parent, self)
        self.loginButton.update_command(self.loginMenu.open)

    def destroy(self):
        """Destroy the widget (removes it from the UI)."""
        self.container.destroy()

    def logout(self):
        print("logging Out..")
        self.loginButton.image = "images/login.png"
        self.loginButton.width = 80
        self.loginButton.tk.config(borderwidth=0, highlightthickness=0)
        self.loginButton.update_command(self.loginMenu.open)
        self.server_info.value = "Not Connected to a Server."
        self.disconnected.set_volume(.1)
        self.disconnected.play()
        globals.client_listen.stop()
