# 代码生成时间: 2025-09-09 13:32:10
# theme_switcher.py
#
# 使用BOTTLE框架实现主题切换功能

from bottle import route, run, request, response, template
import os

# 配置
PORT = 8080
HOST = 'localhost'
THEMES = ['light', 'dark']
CURRENT_THEME = 'light'

# 保存当前主题的文件
THEME_FILE = 'current_theme.txt'

# 读取当前主题
def load_theme():
    if os.path.exists(THEME_FILE):
        with open(THEME_FILE, 'r') as f:
            return f.read().strip()
    return CURRENT_THEME

# 保存主题到文件
def save_theme(theme):
    with open(THEME_FILE, 'w') as f:
        f.write(theme)

# 路由：主页
@route('/')
def index():
    theme = load_theme()
    return template('index', theme=theme)

# 路由：切换主题
@route('/switch_theme', method='POST')
def switch_theme():
    global CURRENT_THEME
    # 获取新的 theme
    new_theme = request.forms.get('theme')
    if new_theme in THEMES:
        # 保存新主题
        save_theme(new_theme)
        CURRENT_THEME = new_theme
        response.status = 200
        return {'status': 'success', 'theme': CURRENT_THEME}
    else:
        response.status = 400
        return {'status': 'error', 'message': 'Invalid theme'}

# 运行服务器
run(host=HOST, port=PORT)
