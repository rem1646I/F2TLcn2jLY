# 代码生成时间: 2025-09-18 14:07:06
# password_encryption_decryption.py
"""
A simple password encryption and decryption tool using the Bottle framework.
"""

import bottle
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from base64 import b64encode, b64decode
from binascii import hexlify, unhexlify
import os
import hashlib

# Configuration
SALT_LENGTH = 16  # bytes
AES_KEY_LENGTH = 32  # bytes

# Initialize Bottle app
app = bottle.Bottle()


def generate_key(password):
    """
    Generate an AES key from a password using PBKDF2.
    :param password: The password to derive the key from.
    :return: A 32-byte AES key.
    """
    salt = os.urandom(SALT_LENGTH)
    key = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    return salt, key


def encrypt_password(password, data):
    """
    Encrypt a password using AES.
    :param password: The password to use for encryption.
    :param data: The data to encrypt.
    :return: A tuple containing the salt, IV, and encrypted data.
    """
    salt, key = generate_key(password)
    iv = os.urandom(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted_data = cipher.encrypt(pad(data.encode(), AES.block_size))
    return salt, iv, encrypted_data


def decrypt_password(password, salt, iv, data):
    """
    Decrypt encrypted data using AES.
    :param password: The password to use for decryption.
    :param salt: The salt used for key derivation.
    :param iv: The initialization vector used for encryption.
    :param data: The encrypted data to decrypt.
    :return: The decrypted data.
    """
    key = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = unpad(cipher.decrypt(data), AES.block_size)
    return decrypted_data.decode()

# Routes

@app.route('/encrypt', method='POST')
def encrypt():
    """
    Endpoint to encrypt a password.
    :return: A JSON response with the encrypted data.
    """
    try:
        password = bottle.request.forms.get('password')
        data = bottle.request.forms.get('data')
        if not password or not data:
            bottle.abort(400, 'Password and data are required.')

        salt, iv, encrypted_data = encrypt_password(password, data)
        response = {
            'salt': b64encode(salt).decode(),
            'iv': b64encode(iv).decode(),
            'encrypted_data': b64encode(encrypted_data).decode()
        }

        return {'status': 'success', 'data': response}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}

@app.route('/decrypt', method='POST')
def decrypt():
    """
    Endpoint to decrypt a password.
    :return: A JSON response with the decrypted data.
    """
    try:
        password = bottle.request.forms.get('password')
        salt = b64decode(bottle.request.forms.get('salt'))
        iv = b64decode(bottle.request.forms.get('iv'))
        encrypted_data = b64decode(bottle.request.forms.get('encrypted_data'))

        if not password or not salt or not iv or not encrypted_data:
            bottle.abort(400, 'Password, salt, IV, and encrypted data are required.')

        decrypted_data = decrypt_password(password, salt, iv, encrypted_data)
        return {'status': 'success', 'data': decrypted_data}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}

# Run the app
if __name__ == '__main__':
    app.run(host='localhost', port=8080)