from server.decryption import verify_password, decrypt_password, get_salt, get_hash
from server.responses.session import get_user_session


def login_test(conn, parts):
    username = parts[1]
    password = decrypt_password(username, parts[2], parts[3], parts[4])

    # Verify credentials
    if verify_password(get_salt(username), get_hash(username), password):
        response = "TEST_SUCCESS|Welcome!|" + get_user_session(username)
    else:
        response = "TEST_FAILURE|Invalid credentials."

    # Send response to client
    conn.sendall(response.encode())

