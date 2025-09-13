# 代码生成时间: 2025-09-13 09:54:44
#!/usr/bin/env python

# -*- coding: utf-8 -*-
"""
Image Resizer - A simple web application to resize images using the Bottle web framework.
"""

from bottle import route, run, request, response, static_file
from PIL import Image
import os

# Define the root directory for the uploaded files
UPLOAD_FOLDER = './uploads/'
OUTPUT_FOLDER = './outputs/'

# Ensure the existence of the upload and output directories
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Configuration for Bottle
bottle_host = 'localhost'
bottle_port = '8080'

# Route for serving static files
@route('/static/<filename:path>')
def serve_static(filename):
    return static_file(filename, root='static')

# Route for the upload form
@route('/')
def index():
    return """
    <h1>Image Resizer</h1>
    <form action="/upload" method="post" enctype="multipart/form-data">
        <input type="file" name="image" multiple>
        <input type="number" name="width" placeholder="Width" required>
        <input type="number" name="height" placeholder="Height" required>
        <input type="submit" value="Resize Image">
    </form>
    """

# Route for handling image uploads and resizing
@route('/upload', method='POST')
def upload():
    image_file = request.files.get('image')
    width = request.forms.get('width')
    height = request.forms.get('height')

    # Check if image file is provided
    if not image_file:
        return "No image file selected."

    try:
        # Open an image file
        image = Image.open(image_file.file)

        # Resize the image
        image = image.resize((int(width), int(height)))

        # Save the resized image
        image_format = image.format.lower()
        output_filename = f"{UPLOAD_FOLDER}{image_file.filename.split('.')[0]}_resized.{image_format}"
        image.save(output_filename)

        # Return success message
        return f"Image resized and saved as {output_filename}."

    except Exception as e:
        # Return error message
        return f"An error occurred: {str(e)}"

# Run the Bottle application
if __name__ == '__main__':
    run(host=bottle_host, port=bottle_port)
