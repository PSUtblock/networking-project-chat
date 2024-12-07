"""File used to encrypt and decrypt messages for the server"""
import base64
import os

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import modes, Cipher, algorithms
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


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

"""
def encrypt_message(user: str, message: str, time: str, key: str) -> dict:
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

    # Concatenate user, message, and time into a single plaintext
    plaintext = f"{user}|{message}|{time}".encode()

    # Encrypt the concatenated plaintext
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()
    tag = encryptor.tag

    return {
        'ciphertext': base64.b64encode(ciphertext).decode(),
        'nonce': base64.b64encode(nonce).decode(),
        'tag': base64.b64encode(tag).decode()
    }


def decrypt_message(key: str, ciphertext: str, nonce: str, tag: str) -> dict:
    # Decode inputs from Base64
    ciphertext = base64.b64decode(ciphertext)
    nonce = base64.b64decode(nonce)
    tag = base64.b64decode(tag)

    # Derive the encryption key using the same method (PBKDF2 with the same salt/nonce)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=nonce,
        iterations=100000,
        backend=default_backend()
    )
    encryption_key = kdf.derive(key.encode())

    # Create AES cipher in GCM mode
    cipher = Cipher(algorithms.AES(encryption_key), modes.GCM(nonce, tag), backend=default_backend())
    decryptor = cipher.decryptor()

    # Decrypt the ciphertext
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    # Split the plaintext back into its components
    user, message, time = plaintext.decode().split("||")

    return {
        "user": user,
        "message": message,
        "time": time
    }

"""