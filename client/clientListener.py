import socket
import threading


class ClientSocketListener:
    def __init__(self, address, port):
        self.address = address
        self.port = port
        self.socket = None
        self.listening = False
        self.listener_thread = None

    # client starts listening for messages from the given server over the given port.
    def start(self):
        if self.listening:
            print("Already listening.")
            return

        try:
            # Create the socket and connect to the server
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.address, self.port))
            print(f"Connected to server at {self.address}:{self.port}")

            # Start the listening thread
            self.listening = True
            self.listener_thread = threading.Thread(target=self.listen, daemon=True)
            self.listener_thread.start()
        except Exception as e:
            print(f"Error starting client: {e}")

    # stops the objects functionalities and closes the connection
    def stop(self):
        """Stop listening and close the socket."""
        self.listening = False
        if self.socket:
            self.socket.close()
            self.socket = None
            print("Stopped listening and closed the connection.")

    # listen function to manage the messages from the server
    def listen(self):
        while self.listening:
            try:
                message = self.socket.recv(1024).decode('utf-8')  # Adjust buffer size as needed
                if message:
                    print(f"Message from server: {message}")
                else:
                    print("Server closed the connection.")
                    self.stop()
            except Exception as e:
                if self.listening:  # Ignore errors if we've stopped listening
                    print(f"Error while listening: {e}")
                self.stop()
                break
