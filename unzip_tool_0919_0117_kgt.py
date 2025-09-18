# 代码生成时间: 2025-09-19 01:17:30
# unzip_tool.py - A simple file unzipping tool using Bottle framework and Python

"""
Unzip Tool: A web-based application to decompress files using Bottle framework.

This application allows users to upload a compressed file and decompress it.
It supports ZIP and GZIP formats.
"""

from bottle import route, run, request, response, template
import os
import shutil
import logging
from zipfile import ZipFile
from gzip import GzipFile
from io import BytesIO

# Define the root directory for the server
ROOT_DIR = '/path/to/root/directory'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Ensure the root directory exists
if not os.path.exists(ROOT_DIR):
    os.makedirs(ROOT_DIR)

@route('/', method='GET')
def index():
    # Serve the HTML form for uploading files
    return template("""
    <html>
        <body>
            <h1>Upload a compressed file</h1>
            <form action="/unzip" method="post" enctype="multipart/form-data">
                <input type="file" name="file" required>
                <input type="submit" value="Unzip">
            </form>
        </body>
    </html>
    """)

@route('/unzip', method='POST')
def unzip_file():
    # Get the uploaded file from the request
    file = request.files.get('file')
    if not file:
        response.status = 400
        return {"error": "No file provided"}

    try:
        # Create a unique filename for the uploaded file
        filename = f'{file.filename}_{int(os.urandom(4).hex(), 16)}'
        filepath = os.path.join(ROOT_DIR, filename)

        # Save the uploaded file
        file.save(filepath)

        # Check if the file is a ZIP file
        if filename.endswith('.zip'):
            with ZipFile(filepath, 'r') as zip_ref:
                zip_ref.extractall(ROOT_DIR)
                logging.info(f'Successfully unzipped {filename}')
                return f"{"Unzipped file saved in \{ROOT_DIR}"}"

        # Check if the file is a GZIP file
        elif filename.endswith('.gz'):
            with GzipFile(filepath, 'rb') as f_in:
                with open(os.path.join(ROOT_DIR, file.filename), 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
                logging.info(f'Successfully decompressed {filename}')
                return f"{"Decompressed file saved in \{ROOT_DIR}"}"

        else:
            response.status = 400
            return {"error": "Unsupported file format"}

    except Exception as e:
        logging.error(f'An error occurred: {e}')
        response.status = 500
        return {"error": "An error occurred while processing the file"}
    finally:
        # Remove the uploaded file after processing
        if os.path.exists(filepath):
            os.remove(filepath)

run(host='localhost', port=8080)
