# 代码生成时间: 2025-08-18 21:32:24
# -*- coding: utf-8 -*-

"""
Text File Analyzer using Python and Bottle framework.
This application takes a text file as input and performs analysis,
including word count, most frequent words, and character count.
"""

from bottle import route, run, request, response
import os
import re
from collections import Counter
from threading import Lock

# Global lock to prevent concurrent access issues during file reading/writing
file_lock = Lock()

@route('/analyze', method='POST')
def analyze_text():
    """Endpoint to analyze the contents of a text file."""
    # Check if the request contains a file
    if 'file' not in request.files:
        response.status = 400
        return {'error': 'No file part in the request'}

    file = request.files['file']
    if file.filename == '':
        response.status = 400
        return {'error': 'No selected file'}

    # Check if the file is a text file
    if not file.filename.endswith('.txt'):
        response.status = 400
        return {'error': 'Only .txt files are allowed'}

    # Read the file content in a thread-safe manner
    with file_lock:
        file_content = file.read().decode('utf-8')

    # Perform text analysis
    try:
        word_count = len(re.findall(r'\w+', file_content))
        most_common_words = Counter(re.findall(r'\w+', file_content)).most_common(10)
        char_count = len(file_content)
    except Exception as e:
        response.status = 500
        return {'error': 'Error during analysis', 'message': str(e)}

    # Prepare the response
    result = {
        'word_count': word_count,
        'most_common_words': most_common_words,
        'character_count': char_count
    }
    return result

# Run the Bottle application on port 8080
run(host='localhost', port=8080)