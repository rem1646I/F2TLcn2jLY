# 代码生成时间: 2025-08-19 09:32:00
from bottle import route, run, request, response, static_file
from PIL import Image
import os
import shutil

# 定义图片尺寸批量调整器的根目录
ROOT_DIR = 'resized_images'

# 检查目录是否存在，如果不存在则创建
if not os.path.exists(ROOT_DIR):
    os.makedirs(ROOT_DIR)

# 定义图片批量调整尺寸的路由
@route('/resizer', method='POST')
def resize_image():
    # 获取上传的文件列表
    files = request.files.getall('file')
    response.content_type = 'application/json'
    result = []
    
    for file in files:
        try:
            # 检查文件是否是图片
            if file.filename.split('.')[-1].lower() not in ['jpg', 'jpeg', 'png', 'gif']:
                result.append({'error': 'Unsupported file format', 'filename': file.filename})
                continue
                
            # 打开并调整图片尺寸
            img = Image.open(file.file)
            img.thumbnail((800, 600))  # 调整到最大800x600
            
            # 保存调整后的图片
            new_filename = os.path.join(ROOT_DIR, file.filename)
            img.save(new_filename)
            
            # 添加成功消息到结果中
            result.append({'success': 'Image resized and saved', 'filename': file.filename})
        except Exception as e:
            # 添加错误消息到结果中
            result.append({'error': str(e), 'filename': file.filename})
    
    return {'status': 'finished', 'results': result}

# 设置静态文件服务目录
@route('/static/<filepath:path>')
def serve_static(filepath):
    return static_file(filepath, root=ROOT_DIR)

# 运行Bottle服务器
run(host='localhost', port=8080, debug=True)

"""
This program is an image size batch resizer using the Bottle framework.

It takes multiple images, resizes them to a maximum of 800x600 pixels, and saves them in a specified directory.

Usage:
- Make a POST request to '/resizer' with images to resize.
- The server will return a JSON response with the status of each image.

Note:
- Only 'jpg', 'jpeg', 'png', and 'gif' file formats are supported.
- The resized images will be saved in the 'resized_images' directory.
"""