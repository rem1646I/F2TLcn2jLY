# 代码生成时间: 2025-08-27 17:37:05
# password_encryption_decryption.py
# 使用Python和Bottle框架实现密码加密解密工具

from bottle import route, run, request, response
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from base64 import b64encode, b64decode
import os
import binascii

# 密钥和IV随机生成
key = get_random_bytes(16)
iv = get_random_bytes(AES.block_size)

# 定义加密函数
def encrypt(plaintext):
    """
    使用AES算法加密明文，返回Base64编码的密文
    :param plaintext: 明文字符串
    :return: 密文字符串
    """
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_data = pad(plaintext.encode(), AES.block_size)
    ciphertext = cipher.encrypt(padded_data)
    return b64encode(ciphertext).decode()

# 定义解密函数
def decrypt(ciphertext):
    """
    使用AES算法解密密文，返回明文字符串
    :param ciphertext: Base64编码的密文字符串
    :return: 明文字符串
    """
    try:
        cipher = AES.new(key, AES.MODE_CBC, iv)
        padded_data = cipher.decrypt(b64decode(ciphertext))
        return unpad(padded_data, AES.block_size).decode()
    except (ValueError, binascii.Error):
        return "Invalid ciphertext"  # 返回无效密文的错误信息

# 定义加密路由
@route('/encrypt', method='POST')
def encrypt_password():
    """
    加密路由，接收POST请求中的明文密码，返回加密后的密文
    """
    plaintext = request.json.get('plaintext')
    if not plaintext:
        response.status = 400
        return {"error": "Missing plaintext"}
    return {"ciphertext": encrypt(plaintext)}

# 定义解密路由
@route('/decrypt', method='POST')
def decrypt_password():
    """
    解密路由，接收POST请求中的密文密码，返回解密后的明文
    """
    ciphertext = request.json.get('ciphertext')
    if not ciphertext:
        response.status = 400
        return {"error": "Missing ciphertext"}
    return {"plaintext": decrypt(ciphertext)}

# 运行Bottle应用
if __name__ == '__main__':
    run(host='localhost', port=8080)