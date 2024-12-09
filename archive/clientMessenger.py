"""
This class handles the messages to the server from the client once a tested connection has been established.
"""

import socket


class ClientMessenger:
    def __init__(self, address, port):
        self.address = address
        self.port = port

    def send_channel_message(self, message: str, channel: str):
        """Send a message to the server."""
        if not globals.session_id:
            print("Error: No session ID. Connect to the server first.")
            return

        try:
            # Create a new socket for sending the message
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as send_socket:
                send_socket.connect((self.address, self.port))
                # Include session ID in the message
                full_message = f"CHANNEL_MESSAGE|{globals.session_id}|{message}|{channel}"
                send_socket.sendall(full_message.encode('utf-8'))
                print(f"Message sent: {message}")
        except Exception as e:
            print(f"Error sending message: {e}")
