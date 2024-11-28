# SeverApp for confab chat application
"""Launch this file to run the server to handle confab chat client requests."""

# import libraries
import socket
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
        # connection information from client
        conn, addr = server_socket.accept()
        with conn:
            print(f"Connected by {addr}")

            # data is populated with information from the client
            data = conn.recv(1024).decode()
            if not data:
                break

            # THIS WILL NEED TO BE MODULARIZED - make py files in the server/responses directory
            # Parse the custom protocol format
            parts = data.split("|")
            if len(parts) == 5 and parts[0] == "LOGIN_TEST":
                login_test(conn, parts)

            else:
                conn.send("ERROR|Invalid request format.".encode())

        print("Connection with", addr, "closed.")