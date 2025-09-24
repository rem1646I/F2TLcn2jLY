# 代码生成时间: 2025-09-24 09:12:27
from bottle import route, run, request, response, template

# 存储主题的字典
themes = {
    'light': 'Light Theme',
    'dark': 'Dark Theme'
}

# 路由装饰器，用于设置和获取主题
@route('/theme/:theme')
def switch_theme(theme):
    # 检查主题是否有效
    if theme not in themes:
        response.status = 404  # 设置状态码为404
        return {'error': 'Invalid theme'}  # 返回错误信息

    # 如果主题有效，设置session中的主题
    request.environ.get('bottle.session').theme = theme
    return {'message': f'Theme switched to {themes[theme]}', 'current_theme': themes[theme]}  # 返回成功信息

# 路由装饰器，用于获取当前主题
@route('/theme')
def get_current_theme():
    current_theme = request.environ.get('bottle.session').get('theme', 'light')  # 默认主题为light
    return {'current_theme': themes.get(current_theme, 'Light Theme')}  # 返回当前主题

# 路由装饰器，用于重置主题
@route('/theme/reset')
def reset_theme():
    request.environ.get('bottle.session').pop('theme', None)  # 删除session中的主题设置
    return {'message': 'Theme reset to default', 'current_theme': 'Light Theme'}  # 返回成功信息

# 主函数，用于启动服务器
def main():
    run(host='localhost', port=8080)  # 启动服务器

# 运行主函数
if __name__ == '__main__':
    main()