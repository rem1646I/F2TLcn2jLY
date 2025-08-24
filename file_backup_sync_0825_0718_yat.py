# 代码生成时间: 2025-08-25 07:18:43
# file_backup_sync.py

# 导入所需的库
import os
import shutil
import bottle
from bottle import route, run, request, response, HTTPError

# 配置Bottle
bottle.TEMPLATES = 'views/'

# 定义全局变量
SOURCE_DIR = '/path/to/source'  # 源目录路径
DESTINATION_DIR = '/path/to/destination'  # 目标目录路径

# 检查源目录和目标目录是否存在，不存在则创建
if not os.path.exists(SOURCE_DIR):
    os.makedirs(SOURCE_DIR)
if not os.path.exists(DESTINATION_DIR):
    os.makedirs(DESTINATION_DIR)

# 定义备份文件的函数
def backup_file(file_path):
    """备份单个文件到目标目录"""
    try:
        shutil.copy2(file_path, DESTINATION_DIR)
        return True
    except Exception as e:
        print(f"备份文件 {file_path} 失败: {e}")
        return False

# 定义同步目录的函数
def sync_directories(source_dir, destination_dir):
    """同步源目录和目标目录"""
    try:
        shutil.copytree(source_dir, destination_dir)
        return True
    except Exception as e:
        print(f"同步目录 {source_dir} 到 {destination_dir} 失败: {e}")
        return False

# 定义Bottle路由处理备份请求
@route('/backup', method='POST')
def backup_request():
    content = request.json
    file_path = content.get('file_path')
    if not file_path:
        raise HTTPError(400, '缺少文件路径参数')
    success = backup_file(file_path)
    if success:
        return {'status': '备份成功'}
    else:
        return {'status': '备份失败'}

# 定义Bottle路由处理同步请求
@route('/sync', method='POST')
def sync_request():
    source_dir_path = request.json.get('source_dir')
    destination_dir_path = request.json.get('destination_dir')
    if not source_dir_path or not destination_dir_path:
        raise HTTPError(400, '缺少源目录或目标目录参数')
    global SOURCE_DIR, DESTINATION_DIR
    SOURCE_DIR = source_dir_path
    DESTINATION_DIR = destination_dir_path
    success = sync_directories(SOURCE_DIR, DESTINATION_DIR)
    if success:
        return {'status': '同步成功'}
    else:
        return {'status': '同步失败'}

# 运行Bottle服务
if __name__ == '__main__':
    run(host='localhost', port=8080, debug=True)