import socket
import threading

from cryptography.fernet import Fernet

class ClientMessenger:
    def __init__(self, address, port, encryption_key):
        self.listen = None
        self.listener_thread = None
        self.socket = None
        self.listening = None
        self.address = address
        self.port = port
        self.current_room = None
        self.message_history = {}  # Room-specific message history
        self.encryption_key = encryption_key

    def encrypt_message(self, message: str) -> str:
        """Encrypt a message using the encryption key."""
        cipher = Fernet(self.encryption_key)
        return cipher.encrypt(message.encode()).decode()

    def decrypt_message(self, encrypted_message: str) -> str:
        """Decrypt a message using the encryption key."""
        cipher = Fernet(self.encryption_key)
        return cipher.decrypt(encrypted_message.encode()).decode()

    def send_channel_message(self, message: str, channel: str):
        """Send a message to a specific channel."""
        ##if not globals().get("session_id"):
           # print("Error: No session ID. Connect to the server first.")
           # return

        try:
            # Create a new socket for sending the message
            #with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as send_socket:
              #  send_socket.connect((self.address, self.port))
                # Encrypt the message
                encrypted_message = self.encrypt_message(message)
                # Include session ID and encrypt message
                full_message = f"CHANNEL_MESSAGE|{globals().get('session_id')}|{encrypted_message}|{channel}"
                self.socket.sendall(full_message.encode("utf-8"))
                print(f"Message sent to {channel}: {message}")
        except Exception as e:
            print(f"Error sending message: {e}")

    def send_to_room(self, room: str, message: str):
        """Send a message to a specific room."""
        if not room:
            print("Error: No room specified.")
            return
        self.send_channel_message(message, room)

        # Save the message in the room's history
        if room not in self.message_history:
            self.message_history[room] = []
        self.message_history[room].append(f"[You] {message}")

    def set_current_room(self, room: str):
        """Set the active room for messaging."""
        self.current_room = room
        print(f"Switched to room: {room}")

    def view_message_history(self, room: str):
        """View message history for a specific room."""
        if room in self.message_history:
            print("\nMessage history for room:", room)
            for msg in self.message_history[room]:
                print(msg)
        else:
            print("No messages in this room.")

    def send_typing_status(self, room: str, status: str):
        """Send typing or status updates to the server."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as send_socket:
                send_socket.connect((self.address, self.port))
                payload = f"STATUS_UPDATE|{globals().get('session_id')}|{room}|{status}"
                send_socket.sendall(payload.encode("utf-8"))
                print(f"Status '{status}' sent for room {room}.")
        except Exception as e:
            print(f"Error sending status: {e}")

    def run(self):
        """Run the messenger to handle user inputs for messaging."""
        
        if self.listening:
            print("Already listening.")
            return

        try:
            # Create the socket and connect to the server
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print(self.address)
            print(self.port)
            self.socket.connect((self.address, self.port))
            print(f"Connected to server at {self.address}:{self.port}")

            # Start the listening thread
            self.listening = True
            self.listener_thread = threading.Thread(target=self.listen, daemon=True)
            self.listener_thread.start()
        except Exception as e:
            print(f"Error starting client: {e}")
            
        while True:
            command = input("Enter message (/switch ROOM, /history ROOM, /exit): ").strip()
            if command.startswith("/switch"):
                room = command.split(" ", 1)[1]
                self.set_current_room(room)
            elif command.startswith("/history"):
                room = command.split(" ", 1)[1]
                self.view_message_history(room)
            elif command == "/exit":
                print("Exiting messenger...")
                break
            elif command.startswith("/message"):
                room = command.split(" ", 1)[1]
                message = command.split(" ")[2]
                self.send_to_room(room, message)
            else:
                if self.current_room:
                    self.send_to_room(self.current_room, command)
                else:
                    print("No active room. Use /switch ROOM to select one.")