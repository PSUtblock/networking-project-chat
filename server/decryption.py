# Decryption functions for the server

# import libraries
import hashlib
from sampleUsers import users
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64


# decrypt_password is used to decrypt the first Test connection sent from the client.
def decrypt_password(key: str, en_password: str, en_nonce: str, en_tag: str) -> str:
    # Decode the inputs from base64
    encrypted_password = base64.b64decode(en_password)
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
    decrypted_password = decrypted.update(encrypted_password) + decrypted.finalize()

    return decrypted_password.decode()


# verify_password compares the hashed password of the user that was made at user registration
def verify_password(stored_salt, stored_hash, password):
    # Convert the stored salt from hex to bytes
    salt = bytes.fromhex(stored_salt)
    # Hash the salt and password
    attempt_hash = hashlib.sha512(salt + password.encode()).hexdigest()
    # Compare the hashes
    return attempt_hash == stored_hash


# get_salt function from the stored users object. Will need to be modified once db is made
def get_salt(user_name):
    return users[user_name][0]


# get_hash function from the stored users object. Will need to be modified once db is made
def get_hash(user_name):
    return users[user_name][1]
