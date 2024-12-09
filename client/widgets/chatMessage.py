from guizero import Box, Text, PushButton
import globals


# ChatMessage class. Use it to post messages in the content box
class ChatMessage:
    def __init__(self, parent, user, message, timestamp):

        # Create a container box for this widget
        self.container = Box(parent)
        self.container.width = "fill"

        # Add a title text
        self.username = Text(self.container, text=user, size=12, color="white", align="left")

        # Add a button with the specified action
        self.text_message = Text(self.container, text=message, size=12, align="left", color="white",  width=100)

        self.time_stamp = Text(self.container, text=timestamp, color="white", size=12, width=20)

    def destroy(self):
        """Destroy the widget (removes it from the UI)."""
        self.container.destroy()