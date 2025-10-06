# 代码生成时间: 2025-10-06 16:48:44
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File Version Control System using Python and Bottle framework.
"""

from bottle import route, run, request, response, static_file
import os
import shutil
import json

# Configuration
FILE_STORAGE_PATH = "./storage/"

# Initialize storage directory
if not os.path.exists(FILE_STORAGE_PATH):
    os.makedirs(FILE_STORAGE_PATH)

"""
Error handling
"""
def handle_error(error):
    if isinstance(error, FileNotFoundError):
        response.status = 404
        return {"error": "File not found"}
    else:
        response.status = 500
        return {"error": "Internal server error"}

"""
Route Definitions
"""
@route('/file', method='POST')
def upload_file():
    """
    Upload a new file or update an existing file.
    """
    try:
        file = request.files.get("file")
        if not file:
            return {"error": "No file provided"}
        file_path = os.path.join(FILE_STORAGE_PATH, file.filename)
        with open(file_path, 'wb') as f:
            f.write(file.file.read())
        return {"message": "File uploaded successfully"}
    except Exception as e:
        return handle_error(e)

@route('/file/<filename:path>', method='GET')
def get_file(filename):
    """
    Retrieve a file by name.
    """
    try:
        file_path = os.path.join(FILE_STORAGE_PATH, filename)
        if not os.path.exists(file_path):
            return handle_error(FileNotFoundError())
        return static_file(filename, root=FILE_STORAGE_PATH, download=True)
    except Exception as e:
        return handle_error(e)

@route('/file/<filename:path>', method='DELETE')
def delete_file(filename):
    """
    Delete a file by name.
    """
    try:
        file_path = os.path.join(FILE_STORAGE_PATH, filename)
        if not os.path.exists(file_path):
            return handle_error(FileNotFoundError())
        os.remove(file_path)
        return {"message": "File deleted successfully"}
    except Exception as e:
        return handle_error(e)

"""
Application Initialization and Run
"""
if __name__ == '__main__':
    run(host='localhost', port=8080, debug=True)
