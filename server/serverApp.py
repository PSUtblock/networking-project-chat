# SeverApp for confab chat application
"""Launch this file to run the server to handle confab chat client requests."""

# import libraries
import socket
import threading

from server.responses.chat import chat_messaging
from server.responses.logging import login_test
from server.responses.session import send_client_list

# TCP server information
HOST = '127.0.0.1'  # Localhost for testing
PORT = 65432  # Arbitrary non-privileged port

# Set to store connected clients
clients = set()
clients_lock = threading.Lock()  # Ensure thread safety when modifying `clients`


def broadcast_message(sender_conn, message):
    """
    Broadcast a message to all connected clients except the sender.

    Args:
        sender_conn: The connection object of the sender.
        message: The message to broadcast (string).
    """
    with clients_lock:
        for client in clients:
            if client != sender_conn:
                try:
                    client.sendall(message.encode())
                except Exception as e:
                    print(f"Error sending message to client {client}: {e}")
                    clients.remove(client)


def handle_client(conn, addr):
    """
    Handle communication with a single client.

    Args:
        conn: The connection object for the client.
        addr: The client's address tuple (host, port).
    """
    print(f"Connected by {addr}")
    with clients_lock:
        clients.add(conn)

    try:
        while True:  # Keep listening for messages from this client
            data = conn.recv(1024).decode()
            if not data:
                print(f"No data received. Closing connection with {addr}.")
                break

            # Parse the custom protocol format
            parts = data.split("|")
            if len(parts) == 5 and parts[0] == "LOGIN_TEST":
                login_test(conn, parts)
            elif len(parts) == 4 and parts[0] == "CHAT_MESSAGE":
                chat_messaging(conn, parts)
                # Broadcast chat message to other clients
                broadcast_message(conn, data)

            elif len(parts) == 1 and parts[0] == "CLIENT_LIST"
                send_client_list(conn)
            else:
                print(f"Error with Received Message: {data}")
                conn.send("ERROR|Invalid request format.".encode())
    except Exception as e:
        print(f"Error with connection {addr}: {e}")
    finally:
        with clients_lock:
            clients.remove(conn)
        conn.close()
        print(f"Connection with {addr} closed.")

# Open socket on the server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print("Server is listening on", HOST, PORT)

    # Accept incoming client connections
    while True:
        conn, addr = server_socket.accept()
        threading.Thread(target=handle_client, args=(conn, addr)).start()
