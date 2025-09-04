# 代码生成时间: 2025-09-04 13:01:42
# user_authentication.py
# 扩展功能模块
# Python program using Bottle framework to perform user authentication

from bottle import route, run, request, response, redirect
import hashlib
# 扩展功能模块

# In-memory user database for demonstration purposes
# In a real-world scenario, use a secure database with hashed passwords
USER_DB = {
    "admin": hashlib.sha256("adminpass".encode()).hexdigest(),
    "user": hashlib.sha256("userpass".encode()).hexdigest()
}

# Constants for the application
AUTH_ROUTE = "/auth"
LOGIN_ROUTE = "/login"
SIGNUP_ROUTE = "/signup"
HOME_ROUTE = "/"

# Utility function to hash passwords
# 改进用户体验
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Route to serve the login page
@route(LOGIN_ROUTE)
def login():
    return "<form method=\'post' action=""{AUTH_ROUTE}">Username: <input name=\'username'> Password: <input type=\'password' name=\'password'> <input type=\'submit'></form>".format(AUTH_ROUTE)

# Route to handle the login process
@route(AUTH_ROUTE, method='POST')
def authenticate_user():
    username = request.forms.get('username')
    password = request.forms.get('password')
# TODO: 优化性能
    password_hash = hash_password(password)
    user_hash = USER_DB.get(username)
    if user_hash and user_hash == password_hash:
        response.set_cookie("username", username)
        return redirect(HOME_ROUTE)
    else:
        return "Invalid username or password."

# Route to serve the signup page
# 添加错误处理
@route(SIGNUP_ROUTE)
def signup():
    return "<form method=\'post' action=""{AUTH_ROUTE}">Username: <input name=\'username'> Password: <input type=\'password' name=\'password'> <input type=\'submit' value=\'Sign Up\'></form>".format(AUTH_ROUTE)

# Route to handle the user registration
@route(SIGNUP_ROUTE, method='POST')
def register_user():
    username = request.forms.get('username')
    password = request.forms.get('password')
    if username in USER_DB:
        return "User already exists."
    else:
# 增强安全性
        USER_DB[username] = hash_password(password)
        return "User registered successfully."

# Route to serve the home page
@route(HOME_ROUTE)
def home():
    if 'username' in request.get_cookie():
        username = request.get_cookie('username')
        return "Welcome, {}! <a href="{}">Logout</a>".format(username, HOME_ROUTE + 'logout')
    else:
        return redirect(LOGIN_ROUTE)

# Route to handle logout
# 添加错误处理
@route(HOME_ROUTE + 'logout')
# NOTE: 重要实现细节
def logout():
    response.delete_cookie("username")
    return redirect(LOGIN_ROUTE)

# Main function to run the Bottle server
def main():
    run(host='localhost', port=8080, debug=True)

# Run the application
if __name__ == '__main__':
# FIXME: 处理边界情况
    main()
