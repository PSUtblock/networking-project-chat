import os.path


def chat_messaging(conn, parts):
    username = parts[1]
    message = parts[2]
    channel = parts[3]
    timestamp = parts[4]

