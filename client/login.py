# Client Login Functions and Login Window UI

""" The login portion of this application is its own file due to the moderate complexity of what
it is doing. In this file a UI element is being made to collect server information from the user.
That data then is used to establish a test connection to the server. This test message is encrypted
and decrypted on the server, with the server's response being a sessionID for the client application
to use to perform future requests until a user quits the client application.

Known Issues:
- Currently it is possible for a user to open the login window twice, which would likely cause issue.
However, testing can still be performed so long as you avoid this."""

# Library Imports
import socket
from guizero import Window, PushButton, TextBox, Text, Box
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os
import base64


# Function to create a login window. This is done from clientApp.py
# when the user clicks the 'login' button in the top UI menu.
def open_login(app, on_login):
    # Window UI initialization
    login_window = Window(app, height=160, width=400, bg="#40466F")
    Box(login_window, align="top", width="fill", height=10)
    Box(login_window, align="left", width=5, height="fill")

    # TextBox Inputs for server_name, server_user, server_password (address,username,password)
    # All fields are set with default testing information and do not need to be changed while testing
    server_box = Box(login_window, align="top", height="fill", width="fill", layout="grid")
    Text(server_box, text="Server :", grid=[0, 0], color="#BCDAE6", size=16, align="left")
    server_name = TextBox(server_box, text="127.0.0.1", align="left", width=33, height=40, grid=[1, 0])
    Text(server_box, text="User :", grid=[0, 1], color="#BCDAE6", size=16, align="left")
    server_user = TextBox(server_box, text="user1", align="left", width=33, height=40, grid=[1, 1])
    Text(server_box, text="Password :", grid=[0, 2], color="#BCDAE6", size=16, align="left")
    server_password = TextBox(server_box, text="password123", align="left", width=33, height=40, grid=[1, 2])

    # Error Message, Test, and Connect UI section
    connection_box = Box(login_window, align="bottom", width="fill", height=100)
    # Target the status_text widget to share errors when testing the connection
    status_text = Text(connection_box, align="top")
    # login_button is hidden until the test button is pushed AND a connection was established to the server
    login_button = PushButton(connection_box, image="images/connect.png", width=90, height=30,
                              command=lambda: login(on_login, server_name.value, login_window), visible=False)
    # test_button handles the first request to the server. Once a connection is confirmed, the button hides
    test_button = PushButton(connection_box, image="images/test.png", width=90, height=30,
                             command=lambda: test_login(test_button, login_button, server_name, server_user,
                                                        server_password, status_text))
    Box(connection_box, align="right", width=60, height=40)


# login Function is used to send data back to the clientApplication.
""" The login function will send back the username, server name/address, and a sessionID generated
when the client tests its connection to the server. The password will no longer be needed and does not need
to be passed and stored while the client application is running. the sessionID will be the confirmation between
the client and server until a user logs out. **see handle_returned_login function within clientApp.py**
"""


def login(on_submit, value, window):
    # Pass the input value back to the main program
    on_submit(value)
    # Close the window after submitting
    window.hide()


# test_login function to encrypt the connection information and retrieve a sessionID
""" This function performs the backbone for all future requests. The users information will be encrypted and nonced
before being sent to the server where the server will handle the decryption and comparison of the login information.
When confirmed the server will send a SessionID back to the client for use in future requests.
"""


def test_login(test_button, login_button, server_name, server_user, server_password, status_text):
    # Conditional to see if user entered all needed information
    if server_name and server_user and server_password:

        # socket creation from the client
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # socket timeout for response.
        client_socket.settimeout(5)

        try:
            # encryption of data starts
            encrypted_data = encrypt_password(server_password.value, server_user.value)
            # log prints to examine values
            print("Encrypted password:", encrypted_data['encrypted_password'])
            print("Nonce:", encrypted_data['nonce'])
            print("Tag:", encrypted_data['tag'])

            # socket is opened - PORT is FIXED, may want to make it a variable
            client_socket.connect((server_name.value, 65432))
            # message to be sent to server
            message = f"LOGIN_TEST|{server_user.value}|{encrypted_data['encrypted_password']}|{encrypted_data['nonce']}|{encrypted_data['tag']}"
            # message sent through socket
            client_socket.sendall(message.encode())

            # Receive response from the server
            # recv accepts different sizes of buffer - does it need to be changed?
            response = client_socket.recv(1024).decode()
            # log prints to examine response
            print("Server response:", response)

            # the message is split on a delimiter so the information can be used
            parts = response.split("|")

            # If successful, the UI will reveal the connect button and hide the test button
            if parts[0] == "TEST_SUCCESS":
                status_text.text_color = "green"
                status_text.value = "Connection was Successful!"
                test_button.hide()
                test_button.disable()
                login_button.visible = True
                login_button.enable()

            # If a failure of credentials, test remains
            else:
                status_text.text_color = "red"
                status_text.value = "Username or Password is Incorrect."

        # exception for if the connection times out
        except socket.timeout:
            status_text.text_color = "red"
            status_text.value = "No response received: socket timed out."

        # exception for any socket error
        except socket.error as e:
            print("Socket error:", e)

        # once the connection is confirmed or denied, the socket closes
        finally:
            client_socket.close()

    else:
        login_button.visible = False
        status_text.text_color = "red"
        status_text.value = "Please enter all fields!"


# encrypt_password function to encrypt the data while it is being transferred
def encrypt_password(password: str, key: str) -> dict:
    nonce = os.urandom(16)

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=nonce,
        iterations=100000,
        backend=default_backend()
    )
    encryption_key = kdf.derive(key.encode())

    cipher = Cipher(algorithms.AES(encryption_key), modes.GCM(nonce), backend=default_backend())
    encryptor = cipher.encryptor()

    encrypted_password = encryptor.update(password.encode()) + encryptor.finalize()

    tag = encryptor.tag

    return {
        'encrypted_password': base64.b64encode(encrypted_password).decode(),
        'nonce': base64.b64encode(nonce).decode(),
        'tag': base64.b64encode(tag).decode()
    }
