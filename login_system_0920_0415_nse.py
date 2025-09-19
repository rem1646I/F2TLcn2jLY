# 代码生成时间: 2025-09-20 04:15:31
from bottle import route, run, request, redirect
from bottle import template

# 假设的用户数据库，实际应用中应该是真实的数据库查询
USER_DATABASE = {
    "user1": "password1",
    "user2": "password2"
}

# 登录页面路由
@route("/login")
def login():
    # 如果用户已经登录，则重定向到首页
    if request.get_cookie("logged_in"):
        redirect("/")
    else:
        # 显示登录表单
        return template("""
        <html>
        <body>
        <form action="/login" method="post">
        Username: <input type="text" name="username" />
        Password: <input type="password" name="password" />
        <input type="submit" value="Login" />
        </form>
        </body>
        </html>""")

# 登录验证路由
@route("/login", method="post")
def do_login():
    username = request.forms.get("username")
    password = request.forms.get("password")
    try:
        # 验证用户名和密码
        if username in USER_DATABASE and USER_DATABASE[username] == password:
            # 设置登录状态的cookie
            response.set_cookie("logged_in", "true")
            redirect("/")
        else:
            return {"error": "Invalid username or password"}
    except Exception as e:
        # 处理异常
        return {"error": str(e)}

# 首页路由，显示登录后的信息
@route("/")
def index():
    if request.get_cookie("logged_in"):
        return "Welcome to the homepage. You are logged in."
    else:
        redirect("/login")

# 退出登录路由
@route("/logout")
def logout():
    response.delete_cookie("logged_in")
    redirect("/login")

if __name__ == "__main__":
    # 运行Bottle应用
    run(host="localhost", port=8080)
