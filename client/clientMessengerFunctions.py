import socket
import threading
from queue import Queue
from typing import Optional, Dict, List

from client.messageHandler import message_handler


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

    def run(self):
        """Initialize the connection and start the listening thread."""
        if self.listening:
            print("Already running.")
            return

        try:
            self._connect()
            self.listening = True
            self.listener_thread = threading.Thread(target=self.listen_to_server, daemon=True)
            self.listener_thread.start()

        except Exception as e:
            print(f"Error starting messenger: {e}")
            self.stop()

    def _connect(self):
        """Establish a connection to the server."""
        if self.socket:
            self.socket.close()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.address, self.port))
        print(f"Connected to server at {self.address}:{self.port}")

    def send_message(self, message_data):
        """Send a message to the server."""
        try:
            if not self.socket:
                raise Exception("No active connection")

            # Convert message to string and send
            message = f"CHAT_MESSAGE|{message_data}"
            self.socket.sendall(message.encode('utf-8'))

        except (socket.error, Exception) as e:
            print(f"Error sending message: {e}")
            self.stop()

    def listen_to_server(self):
        """Listen for messages from the server."""
        try:
            while self.listening:
                if self.socket:
                    try:
                        data = self.socket.recv(1024).decode('utf-8')
                        if data:
                            print(f"Message from server: {data}")
                            self.message_queue.put(data)
                            message_handler(data)
                        else:
                            print("Server closed the connection.")
                            self.stop()
                            break
                    except socket.error as e:
                        print(f"Socket error while receiving: {e}")
                        self.stop()
                        break
                else:
                    print("No active connection.")
                    self.stop()
                    break
        except Exception as e:
            print(f"Error in listener thread: {e}")
            self.stop()

    def stop(self):
        """Stop the connection and listener thread."""
        self.listening = False
        if self.socket:
            try:
                self.socket.close()
            except Exception as e:
                print(f"Error closing socket: {e}")
            self.socket = None
        print("Connection closed.")
