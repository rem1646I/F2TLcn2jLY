# 代码生成时间: 2025-09-09 09:45:51
from bottle import route, run, request, response
import os
from PIL import Image
from io import BytesIO
import mimetypes

# 定义批量调整图片尺寸的接口
@route('/resize', method='POST')
def resize_images():
    # 获取上传的文件列表
    files = request.files
    if not files: raise ValueError("No files provided")
    
    target_size = request.forms.get('target_size')
    if not target_size: raise ValueError("Target size is required")
    
    # 将目标尺寸字符串分割成宽和高的整数
    try:
        width, height = map(int, target_size.split('x'))
    except ValueError: raise ValueError("Invalid target size format. Use 'WIDTHxHEIGHT'")
    
    # 初始化响应内容
    response.content_type = 'application/json'
    results = []
    
    # 遍历上传的文件
    for filename, file in files.items():
        try:
            # 打开图片文件
            image = Image.open(file)
            
            # 调整图片尺寸
            image = image.resize((width, height), Image.ANTIALIAS)
            
            # 将调整后的图片保存到字节流中
            output = BytesIO()
            image.save(output, format="JPEG", quality=85)
            output.seek(0)
            
            # 将字节流添加到响应内容中
            mimetype = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
            results.append({
                'filename': filename,
                'mimetype': mimetype,
                'data': output.read().hex()  # 将字节数据转换为十六进制字符串
            })
        except IOError:  # 处理图片打开失败
            results.append({'error': 'Failed to process image'})
        except Exception as e:  # 其他错误
            results.append({'error': str(e)})
    
    return {'results': results}  # 返回包含结果的JSON对象

# 设置静态文件目录
@route('/images/<filename:path>')
def images(filename):  # 静态文件路由
    return static_file(filename, root='images')

# 运行服务器
run(host='localhost', port=8080, debug=True)
