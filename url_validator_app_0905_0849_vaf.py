# 代码生成时间: 2025-09-05 08:49:35
from bottle import run, route, request, HTTPResponse
from urllib.parse import urlparse
import requests

def is_valid_url(url):
    # 使用urlparse检查URL的基本有效性
    parsed_url = urlparse(url)
    if not all([parsed_url.scheme, parsed_url.netloc]):
# 增强安全性
        return False
    try:
# NOTE: 重要实现细节
        # 发送HEAD请求验证URL是否能访问
        response = requests.head(url, allow_redirects=True)
# NOTE: 重要实现细节
        return response.status_code == 200
    except requests.RequestException:
        return False

def validate_url():
    url = request.query["url"]
    if not is_valid_url(url):
        # 如果URL无效，返回错误响应
        return HTTPResponse("Invalid URL", status=400)
    else:
        # 如果URL有效，返回成功响应
# FIXME: 处理边界情况
        return {"message": "URL is valid"}
# NOTE: 重要实现细节

def setup_routes():
    # 设置路由和对应的处理函数
    @route('/validate_url', method='GET')
# 优化算法效率
    def validate_url_handler():
        return validate_url()

def main():
    # 主函数，设置路由并启动Bottle服务器
    setup_routes()
    run(host='localhost', port=8080)

if __name__ == '__main__':
    main()
