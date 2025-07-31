# 代码生成时间: 2025-08-01 04:32:41
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Password Encryption and Decryption Tool

This tool provides a simple web application using Bottle framework to
encrypt and decrypt passwords.
"""

from bottle import route, run, request, response
from cryptography.fernet import Fernet

# Generate a key for encryption and decryption. This should be saved securely.
# For demonstration purposes, we're generating a new key every time.
# In a production environment, you should keep the key secure and consistent.
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Route for encrypting a password
@route('/encrypt', method='POST')
def encrypt_password():
    try:
        # Get the password from the request
        password = request.json.get('password')
        if not password:
            response.status = 400
            return {"error": "Password is required."}
        # Encrypt the password
        encrypted_password = cipher_suite.encrypt(password.encode())
        # Return the encrypted password
        return {"encrypted_password": encrypted_password.decode()}
    except Exception as e:
        # Handle any errors that occur during encryption
        response.status = 500
        return {"error": str(e)}

# Route for decrypting a password
@route('/decrypt', method='POST')
def decrypt_password():
    try:
        # Get the encrypted password from the request
        encrypted_password = request.json.get('encrypted_password')
        if not encrypted_password:
            response.status = 400
            return {"error": "Encrypted password is required."}
        # Decrypt the password
        decrypted_password = cipher_suite.decrypt(encrypted_password.encode())
        # Return the decrypted password
        return {"decrypted_password": decrypted_password.decode()}
    except Exception as e:
        # Handle any errors that occur during decryption
        response.status = 500
        return {"error": str(e)}

# Run the Bottle application on port 8080
run(host='localhost', port=8080)