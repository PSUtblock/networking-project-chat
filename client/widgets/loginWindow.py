from guizero import Window, Box, PushButton, Text, TextBox
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os
import base64
import socket
import globals


class LoginWindow:
    def __init__(self, parent, menu):

        self.container = Window(parent, height=160, width=400, bg="#40466F")
        self.topPad = Box(self.container, align="top", width="fill", height=10)
        self.leftPad = Box(self.container, align="left", width=5, height="fill")

        self.server_box = Box(self.container, align="top", height="fill", width="fill", layout="grid")
        self.server_label = Text(self.server_box, text="Server :", grid=[0, 0], color="#BCDAE6", size=16, align="left")
        self.server_name = TextBox(self.server_box, text="127.0.0.1", align="left", width=33, height=40, grid=[1, 0])
        self.user_label = Text(self.server_box, text="User :", grid=[0, 1], color="#BCDAE6", size=16, align="left")
        self.server_user = TextBox(self.server_box, text="user1", align="left", width=33, height=40, grid=[1, 1])
        self.password_label = Text(self.server_box, text="Password :", grid=[0, 2], color="#BCDAE6", size=16,
                                   align="left")
        self.server_password = TextBox(self.server_box, text="password123", align="left", width=33, height=40,
                                       grid=[1, 2])

        self.status_box = Box(self.container, align="bottom", width="fill", height=100)
        self.status_text = Text(self.status_box, align="top")

        self.login_button = PushButton(self.status_box, image="images/test.png", width=90, height=30,
                                       command="nothing")
        self.login_button.update_command(self.test_login, args=[menu])

        self.container.visible = False

    def open(self, menu):
        self.status_text.value = ""
        self.login_button.image = "images/test.png"
        self.login_button.width = 90
        self.login_button.height = 30
        self.login_button.update_command(self.test_login, args=[menu])
        self.container.show()

    def connect(self, menu):
        self.login_button.update_command(self.container.hide)
        menu.loginButton.image = "images/logout.png"
        menu.loginButton.width = 80
        menu.loginButton.tk.config(borderwidth=0, highlightthickness=0)
        menu.loginButton.update_command(menu.logout)
        menu.connected.set_volume(.1)
        menu.connected.play()
        ## globals.client_listen.start()
        globals.client_messenger.run()
        self.container.visible = False

    def test_login(self, menu):
        if self.server_name.value and self.server_user.value and self.server_password.value:

            # socket creation from the client
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # socket timeout for response.
            client_socket.settimeout(5)

            try:
                # encryption of data starts
                encrypted_data = encrypt_password(self.server_password.value, self.server_user.value)
                # log prints to examine values
                print("Encrypted password:", encrypted_data['encrypted_password'])
                print("Nonce:", encrypted_data['nonce'])
                print("Tag:", encrypted_data['tag'])

                # socket is opened - PORT is FIXED, may want to make it a variable
                client_socket.connect((self.server_name.value, 65432))
                # message to be sent to server
                message = f"LOGIN_TEST|{self.server_user.value}|{encrypted_data['encrypted_password']}|{encrypted_data['nonce']}|{encrypted_data['tag']}"
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
                    self.status_text.text_color = "green"
                    self.status_text.value = "Connection was Successful!"
                    self.login_button.image = "images/connect.png"
                    self.login_button.height = 30
                    self.login_button.width = 90
                    self.login_button.update_command(self.connect, [menu])
                    globals.session_id = parts[2]
                    globals.client_listen.address = self.server_name.value
                    globals.client_listen.port = 65432
                    globals.client_messenger.address = self.server_name.value
                    globals.client_messenger.port = 65432
                    globals.client_username = self.server_user.value


                # If a failure of credentials, test remains
                else:
                    self.status_text.text_color = "red"
                    self.status_text.value = "Username or Password is Incorrect."

            # exception for if the connection times out
            except socket.timeout:
                self.status_text.text_color = "red"
                self.status_text.value = "No response received: socket timed out."

            # exception for any socket error
            except socket.error as e:
                print("Socket error:", e)

            # once the connection is confirmed or denied, the socket closes
            finally:
                client_socket.close()

        else:
            self.status_text.text_color = "red"
            self.status_text.value = "Please enter all fields!"


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
