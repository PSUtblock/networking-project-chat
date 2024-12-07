import socket
import threading
import json
from queue import Queue
from typing import Optional, Dict, List
import globals
import datetime

class MessengerFunctions:
    def __init__(self, address: str, port: int, encryption_key: bytes):
        self.address = address
        self.port = port
        self.socket: Optional[socket.socket] = None
        self.listening = False
        self.listener_thread: Optional[threading.Thread] = None
        self.message_queue = Queue()
        self.current_room: Optional[str] = None
        self.message_history: Dict[str, List[dict]] = {}
        self.encryption_key = encryption_key  # Using the 32-bit key passed from clientApp

    # Opens a socket for listening to messages from the server
    def run(self):
        """Initialize the connection and start listening thread"""
        if self.listening:
            print("Already running.")
            return

        try:
            # Create the socket and connect to the server
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.address, self.port))
            print(f"Connected to server at {self.address}:{self.port}")


        except Exception as e:
            print(f"Error starting messenger: {e}")
            return False

    def send_message(self, message_data):
        """Send a message to the server"""
        try:
            if not self.socket:
                raise Exception("No active connection")

            # Convert message to string and send
            message = f"CHAT_MESSAGE|{message_data}"
            self.socket.sendall(message.encode('utf-8'))

        except Exception as e:
            print(f"Error sending message: {e}")
            self.stop()  # Close connection on error
            raise
