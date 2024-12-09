from server.serverApp import clients


def send_client_list(conn):
    """Send the list of connected clients to a specific client."""
    client_list = [str(addr) for addr in clients.keys()]
    client_list_message = "CLIENT_LIST|" + ",".join(client_list)
    try:
        conn.send(client_list_message.encode('utf-8'))
        print(f"Sent client list: {client_list_message}")
    except Exception as e:
        print(f"Error sending client list: {e}")

