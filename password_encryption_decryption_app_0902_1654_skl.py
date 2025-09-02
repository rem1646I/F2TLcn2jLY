# 代码生成时间: 2025-09-02 16:54:51
from bottle import route, run, request, response
from cryptography.fernet import Fernet
import base64
import os

# Generate a key for encryption. This key should be kept secret.
def generate_key():
    return Fernet.generate_key()

# Load the key from a file if it exists, otherwise generate a new one.
def load_or_generate_key():
    key_file = 'secret.key'
    if os.path.exists(key_file):
        with open(key_file, 'rb') as key_file:
            return key_file.read()
    else:
        key = generate_key()
        with open(key_file, 'wb') as key_file:
            key_file.write(key)
        return key

# Encrypt a password using the loaded key.
def encrypt_password(password):
    fernet = Fernet(load_or_generate_key())
    return fernet.encrypt(password.encode()).decode()

# Decrypt a password using the loaded key.
def decrypt_password(encrypted_password):
    fernet = Fernet(load_or_generate_key())
    try:
        return fernet.decrypt(encrypted_password.encode()).decode()
    except Exception as e:
        return f'Failed to decrypt: {e}'

# Route to handle encryption.
@route('/encrypt', method='POST')
def encrypt():
    response.content_type = 'application/json'
    try:
        password = request.json.get('password')
        if not password:
            return {'error': 'Password is required'}
        encrypted = encrypt_password(password)
        return {'encrypted': encrypted}
    except Exception as e:
        return {'error': str(e)}

# Route to handle decryption.
@route('/decrypt', method='POST')
def decrypt():
    response.content_type = 'application/json'
    try:
        encrypted_password = request.json.get('encrypted_password')
        if not encrypted_password:
            return {'error': 'Encrypted password is required'}
        decrypted = decrypt_password(encrypted_password)
        return {'decrypted': decrypted}
    except Exception as e:
        return {'error': str(e)}

# Run the server
if __name__ == '__main__':
    run(host='localhost', port=8080, debug=True)
