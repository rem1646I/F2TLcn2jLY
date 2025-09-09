# 代码生成时间: 2025-09-09 22:57:37
from bottle import route, run, request, response
import os
import zipfile
import shutil

# Define the path to store the uploaded files and extracted files
UPLOAD_FOLDER = 'uploads/'
EXTRACT_FOLDER = 'extracted/'

# Ensure the upload and extract folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(EXTRACT_FOLDER, exist_ok=True)

# Home route
@route('/')
def index():
    return "Welcome to the File Decompression Tool"

# Route to handle file uploads and decompression
@route('/decompress', method='POST')
def decompress():
    # Get the uploaded file
    file = request.files.get('file')
    if not file:
        return {'error': 'No file uploaded'}
    
    # Define file path
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    
    try:
        # Check if the file is a zip file
        if file.filename.endswith('.zip'):
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                # Extract all the contents into the extract folder
                zip_ref.extractall(EXTRACT_FOLDER)
            response.status = 200
            return {'message': 'File decompressed successfully'}
        else:
            response.status = 400
            return {'error': 'File is not a zip file'}
    except zipfile.BadZipFile:
        response.status = 500
        return {'error': 'Failed to decompress the file'}
    finally:
        # Remove the uploaded file after processing
        os.remove(file_path)

# Start the Bottle server
if __name__ == '__main__':
    run(host='localhost', port=8080)
