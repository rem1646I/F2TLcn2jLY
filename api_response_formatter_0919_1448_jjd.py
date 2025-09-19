# 代码生成时间: 2025-09-19 14:48:01
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
API响应格式化工具，使用Bottle框架。
"""

from bottle import route, run, response, request, HTTPResponse

# API响应格式化工具
class ApiResponseFormatter:
    """
    格式化API响应的工具类。
    
    提供格式化成功和错误响应的方法。
    """
    def __init__(self):
        pass

    def success_response(self, data=None, message="Success"):
        """
        格式化成功的响应。
        
        :param data: 响应数据
        :param message: 响应消息
        :return: 格式化的JSON响应
        """
        response_dict = {
            "status": "success",
            "message": message,
            "data": data
        }
        return self._format_response(response_dict)

    def error_response(self, error_code, message="Error"):
        """
        格式化错误的响应。
        
        :param error_code: 错误代码
        :param message: 错误消息
        :return: 格式化的JSON响应
        """
        response_dict = {
            "status": "error",
            "error_code": error_code,
            "message": message
        }
        return self._format_response(response_dict)

    def _format_response(self, response_dict):
        """
        将字典格式化为JSON响应。
        
        :param response_dict: 要格式化的字典
        :return: 格式化的JSON响应
        """
        response.content_type = 'application/json'
        return response_dict

# 创建ApiResponseFormatter实例
formatter = ApiResponseFormatter()

# 定义API路由
@route("/api/success")
def api_success():
    """
    成功响应的API。
    
    :return: 成功的JSON响应
    """
    return formatter.success_response(data={"key": "value"})

@route("/api/error")
def api_error():
    """
    错误响应的API。
    
    :return: 错误的JSON响应
    """
    return formatter.error_response(error_code=404)

# 运行Bottle服务器
if __name__ == "__main__":
    run(host="localhost", port=8080, debug=True)