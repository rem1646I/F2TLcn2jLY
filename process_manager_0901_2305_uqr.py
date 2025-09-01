# 代码生成时间: 2025-09-01 23:05:47
from bottle import route, run, request, response
import subprocess
import os
import json

# 定义一个全局字典来存储进程信息
process_info = {}

# 获取所有进程信息的路由
@route('/processes', method='GET')
def get_processes():
    """
    返回系统中所有进程的信息。
    """
    try:
        # 使用subprocess调用系统命令获取进程信息
        output = subprocess.check_output(['ps', '-aux']).decode('utf-8')
        response.content_type = 'application/json'
        return json.dumps({'processes': output})
    except Exception as e:
        return json.dumps({'error': str(e)}), 500

# 启动一个新进程的路由
@route('/process', method='POST')
def start_process():
    """
    接收POST请求来启动一个新的进程。
    """
    try:
        # 从请求中获取要启动的命令
        data = request.json
        command = data['command']
        # 启动进程
        process = subprocess.Popen(command, shell=True)
        # 将进程信息存储到全局字典中
        process_info[process.pid] = {'command': command, 'pid': process.pid}
        return json.dumps({'pid': process.pid}), 201
    except Exception as e:
        return json.dumps({'error': str(e)}), 400

# 终止一个进程的路由
@route('/process/<pid:int>', method='DELETE')
def stop_process(pid):
    """
    通过进程ID终止一个进程。
    """
    try:
        # 检查进程是否存在于全局字典中
        if pid in process_info:
            # 终止进程
            os.kill(pid, 9)
            # 从全局字典中移除进程信息
            del process_info[pid]
            return json.dumps({'message': 'Process terminated'}), 200
        else:
            return json.dumps({'error': 'Process not found'}), 404
    except Exception as e:
        return json.dumps({'error': str(e)}), 500

# 运行Bottle服务器
if __name__ == '__main__':
    run(host='localhost', port=8080, debug=True)