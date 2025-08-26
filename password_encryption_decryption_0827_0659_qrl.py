# 代码生成时间: 2025-08-27 06:59:01
from bottle import route, run, request, response
from cryptography.fernet import Fernet

# 初始化密钥和Fernet实例
def generate_key():
    """生成密钥"""
    return Fernet.generate_key()

def load_key():
    """从文件加载密钥"""
    try:
        with open('key.key', 'rb') as key_file:
            return key_file.read()
    except FileNotFoundError:
        return generate_key()

key = load_key()
cipher_suite = Fernet(key)

@route('/')
def index():
    """主页面"""
    return 'Welcome to the Password Encryption/Decryption Tool'

@route('/api/encrypt', method='POST')
def encrypt():
    """加密密码"""
    password = request.json.get('password')
    if not password:
        response.status = 400
        return {'error': 'No password provided'}
    encrypted_password = cipher_suite.encrypt(password.encode())
    return {'encrypted_password': encrypted_password.decode()}

@route('/api/decrypt', method='POST')
def decrypt():
    """解密密码"""
    encrypted_password = request.json.get('encrypted_password')
    if not encrypted_password:
        response.status = 400
        return {'error': 'No encrypted password provided'}
    try:
        decrypted_password = cipher_suite.decrypt(encrypted_password.encode())
        return {'decrypted_password': decrypted_password.decode()}
    except Exception as e:
        response.status = 500
        return {'error': str(e)}

if __name__ == '__main__':
    run(host='localhost', port=8080, debug=True)