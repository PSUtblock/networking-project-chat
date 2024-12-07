import os.path


def chat_messaging(conn, parts):
    username = parts[1]
    message = parts[2]
    timestamp = parts[3]

    """
      Handle a CHAT_MESSAGE request.

      Args:
          conn: The connection object for the client.
          parts: Parsed parts of the message.
      """
    # Example handling
    print("Handling CHAT_MESSAGE:", parts)
    conn.send(f"CHAT_MESSAGE|RECEIVED|{username}|{message}|{timestamp}".encode())



