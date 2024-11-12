# Sample user database with hashed passwords
""" These test objects should be replaced with some actual database to store and persist the data."""

# imported libraries
import hashlib
import os
import secrets


# hash_password function hashes the password of a new user on registration with a random salt.
def hash_password(password):
    salt = os.urandom(16)

    hashed_password = hashlib.sha512(salt + password.encode()).hexdigest()

    return salt.hex(), hashed_password

# users will be stored in something that can hold the username, saltvalue, and hashed password
users = {
    "user1": hash_password("password123"),
    "user2": hash_password("securepassword")
}

# user sessions will be stored when client applications establish test connections. these
# sessions will then be used to confirm future requests from the client.
user_sessions = {

}
