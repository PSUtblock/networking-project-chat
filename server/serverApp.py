# SeverApp for confab chat application
"""Launch this file to run the server to handle confab chat client requests."""

# import libraries
import socket

from server.responses.chat import chat_messaging
from server.responses.logging import login_test

# TCP server information
HOST = '127.0.0.1'  # Localhost for testing
PORT = 65432  # Arbitrary non-privileged port

# Open socket on the server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print("Server is listening on", HOST, PORT)

    # Listening Loop
    while True:
        # Accept connection from client
        conn, addr = server_socket.accept()
        print(f"Connected by {addr}")

        try:
            while True:  # Keep listening for messages from this connection
                # Receive data from client
                data = conn.recv(1024).decode()
                if not data:
                    print(f"No data received. Closing connection with {addr}.")
                    break

                # Parse the custom protocol format
                parts = data.split("|")
                if len(parts) == 5 and parts[0] == "LOGIN_TEST":
                    login_test(conn, parts)
                elif len(parts) == 5 and parts[0] == "CHAT_MESSAGE":
                    chat_messaging(conn, parts)
                else:
                    print(f"Error with Received Message: {data}")
                    conn.send("ERROR|Invalid request format.".encode())
        except Exception as e:
            print(f"Error with connection {addr}: {e}")
        finally:
            # Close connection when the client disconnects or an error occurs
            conn.close()
            print(f"Connection with {addr} closed.")

