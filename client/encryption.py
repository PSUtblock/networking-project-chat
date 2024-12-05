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

    encrypted_user = encryptor.update(user.encode()) + encryptor.finalize()
    encrypted_message = encryptor.update(message.encode()) + encryptor.finalize()
    encrypted_time = encryptor.update(time.encode()) + encryptor.finalize()

    tag = encryptor.tag

    return {
        'encrypted_password': base64.b64encode(encrypted_user).decode(),
        'encrypted_message': base64.b64encode(encrypted_message).decode(),
        'encrypted_time': base64.b64encode(encrypted_time).decode(),
        'nonce': base64.b64encode(nonce).decode(),
        'tag': base64.b64encode(tag).decode()
    }


def decrypt_message(key: str, en_user: str, en_message: str, en_time: str, en_nonce: str, en_tag: str) -> dict:
    # Decode the inputs from base64
    encrypted_user = base64.b64decode(en_user)
    encrypted_message = base64.b64decode(en_message)
    encrypted_time = base64.b64decode(en_time)
    nonce = base64.b64decode(en_nonce)
    tag = base64.b64decode(en_tag)

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
    decrypted = cipher.decryptor()

    # Decrypt the password
    decrypted_message = decrypted.update(encrypted_message) + decrypted.finalize()
    decrypted_user = decrypted.update(encrypted_user) + decrypted.finalize()
    decrypted_time = decrypted.update(encrypted_time) + decrypted.finalize()

    return {
        "user": decrypted_user,
        "message": decrypted_message,
        "date": encrypted_time
    }
