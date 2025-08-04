# 代码生成时间: 2025-08-04 19:13:02
from bottle import route, run, request, response, template
import hashlib

# 配置Bottle应用
app = application = default_app = Bottle()

# 模拟数据库存储的用户信息
users = {
    "admin": {"password": "5f4dcc3b5aa765d61d8327deb882cf99"} # 密码为123456的MD5值
}

# 用户注册路由
@route('/register', method='POST')
def register_user():
    username = request.forms.get('username')
    password = request.forms.get('password')

    # 检查用户名是否已存在
    if username in users:
        return template("Registration failed: Username already exists.")
    # 检查密码是否为空
    if not password:
        return template("Registration failed: Password cannot be empty.")

    # 将密码进行MD5加密后存储
    users[username] = {"password": hashlib.md5(password.encode()).hexdigest()}
    return template("Registration successful.")

# 用户登录路由
@route('/login', method='POST')
def login_user():
    username = request.forms.get('username')
    password = request.forms.get('password')

    # 验证用户信息
    if username not in users or users[username]['password'] != hashlib.md5(password.encode()).hexdigest():
        return template("Login failed: Incorrect username or password.")

    # 设置session
    response.set_cookie('username', username)
    return template("Login successful.")

# 登出路由
@route('/logout')
def logout_user():
    response.set_cookie('username', '', path='/', max_age=0)
    return template("Logout successful.")

# 需要认证的路由
@route('/admin')
def admin_panel():
    username = request.get_cookie('username')
    if not username or username not in users:
        return template("Access denied. Please login first.")
    return template("Welcome to the admin panel!")

# 运行Bottle应用
if __name__ == '__main__':
    run(app, host='localhost', port=8080)
