# 代码生成时间: 2025-08-23 09:01:34
# data_analysis_app.py

"""
统计数据分析器，使用Python和Bottle框架实现。
"""

from bottle import Bottle, run, request, response, static_file
import json
import pandas as pd
import numpy as np

# 创建Bottle应用实例
app = Bottle()

"""
路由：返回静态文件
"""
@app.route('/')
def serve_static():
    return static_file('index.html', root='static')

"""
路由：处理数据上传
"""
@app.route('/upload', method='POST')
def upload_data():
    # 获取上传的文件
    file = request.files.get('data_file')
    if file is None:
        response.status = 400
        return json.dumps({'error': 'No file provided'})
    try:
        # 读取文件内容
        data = pd.read_csv(file.file)
        # 调用数据分析函数
        analysis_result = analyze_data(data)
        # 返回分析结果
        return json.dumps({'status': 'success', 'result': analysis_result})
    except Exception as e:
        # 处理读取文件时的异常
        response.status = 500
        return json.dumps({'error': str(e)})

"""
数据分析函数
"""
def analyze_data(data):
    """
    对数据进行分析，返回统计结果。
    :param data: pandas DataFrame对象，包含上传的数据。
    :return: 包含统计结果的字典。
    """
    # 计算基本统计量
    stats = {
        'mean': data.mean().to_dict(),
        'std': data.std().to_dict(),
        'max': data.max().to_dict(),
        'min': data.min().to_dict()
    }
    # 计算相关性矩阵
    correlation_matrix = data.corr().to_dict()
    # 将相关性矩阵转换为易于阅读的格式
    correlation_result = {
        key: {str(k): value for k, value in value.items()}
        for key, value in correlation_matrix.items()
    }
    # 返回统计结果
    return {'stats': stats, 'correlation': correlation_result}


# 运行应用
if __name__ == '__main__':
    run(app, host='localhost', port=8080)