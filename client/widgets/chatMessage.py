from guizero import Box, Text, PushButton
import globals


# Define a class for a custom UI component
class ChatMessage:
    def __init__(self, parent, button_text, button_action):

        # Create a container box for this widget
        self.container = Box(parent)
        self.container.width = "fill"

        # Add a title text
        self.username = Text(self.container, text=globals.client_username, size=12, color="blue", align="left")

        # Add a button with the specified action
        self.button = PushButton(self.container, text=button_text, command=button_action, align="left", width="fill")

        self.timetamp = Text(self.container, text="nvm")

    def destroy(self):
        """Destroy the widget (removes it from the UI)."""
        self.container.destroy()