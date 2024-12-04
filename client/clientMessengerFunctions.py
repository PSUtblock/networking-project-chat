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

            # Start the listening thread
            self.listening = True
            self.listener_thread = threading.Thread(target=self._listen, daemon=True)
            self.listener_thread.start()

            return True
        except Exception as e:
            print(f"Error starting messenger: {e}")
            return False

    def _listen(self):
        """Listen for incoming messages from server"""
        while self.listening:
            try:
                message = self.socket.recv(1024).decode('utf-8')
                if message:
                    print(f"Received from server: {message}")
                    self._handle_message(message)
                else:
                    print("Server closed the connection.")
                    self.stop()
                    break
            except Exception as e:
                if self.listening:
                    print(f"Error while listening: {e}")
                self.stop()
                break

    def _handle_message(self, message: str):
        """Process received messages"""
        try:
            # Add message handling logic here based on server's message format
            # For now, just print the message as server is echoing
            print(f"Handling message: {message}")
        except Exception as e:
            print(f"Error handling message: {e}")

    def send_channel_message(self, message: str, channel: str):
        """Send a message to a specific channel"""
        if not globals.session_id:
            print("Error: No session ID. Connect to the server first.")
            return False

        try:
            # Format the message according to your protocol
            message_data = {
                'type': 'channel_message',
                'session_id': globals.session_id,
                'channel': channel,
                'content': message,
                'username': globals.client_username
            }

            # Send the message
            self._send_message(message_data)

            # Store in local history
            self._add_to_history(channel, {
                'username': globals.client_username,
                'content': message,
                'timestamp': datetime.datetime.now().isoformat()
            })

            return True

        except Exception as e:
            print(f"Error sending message: {e}")
            return False

    def send_message(self, message_data, current_channel):
        """Send a message to the server"""
        try:
            if not self.socket:
                raise Exception("No active connection")

            # Convert message to string and send
            message = f"CHAT_MESSAGE|{globals.session_id}|{message_data}|{current_channel}{datetime.datetime.now().isoformat()}"
            self.socket.sendall(message.encode('utf-8'))

        except Exception as e:
            print(f"Error sending message: {e}")
            self.stop()  # Close connection on error
            raise

    def join_room(self, room_name: str) -> bool:
        """Join a chat room"""
        try:
            message_data = {
                'type': 'join_room',
                'session_id': globals.session_id,
                'room': room_name
            }

            self._send_message(message_data)
            self.current_room = room_name

            if room_name not in self.message_history:
                self.message_history[room_name] = []
            return True

        except Exception as e:
            print(f"Error joining room: {e}")
            return False

    def _add_to_history(self, room: str, message: dict):
        """Add a message to the room's history"""
        if room not in self.message_history:
            self.message_history[room] = []
        self.message_history[room].append(message)

        # Keep last 100 messages
        if len(self.message_history[room]) > 100:
            self.message_history[room] = self.message_history[room][-100:]

    def send_typing_status(self, room: str, is_typing: bool):
        """Send typing status updates"""
        try:
            message_data = {
                'type': 'typing_status',
                'session_id': globals.session_id,
                'room': room,
                'is_typing': is_typing,
                'username': globals.client_username
            }

            self._send_message(message_data)

        except Exception as e:
            print(f"Error sending typing status: {e}")

    def stop(self):
        """Stop the messenger and clean up"""
        self.listening = False
        if self.socket:
            try:
                self.socket.shutdown(socket.SHUT_RDWR)
            except:
                pass
            self.socket.close()
            self.socket = None
        if self.listener_thread and self.listener_thread.is_alive():
            self.listener_thread.join(timeout=1)
        print("Messenger stopped")

    def get_room_history(self, room: str) -> List[dict]:
        """Get message history for a room"""
        return self.message_history.get(room, [])