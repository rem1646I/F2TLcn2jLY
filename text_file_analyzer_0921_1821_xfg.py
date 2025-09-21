# 代码生成时间: 2025-09-21 18:21:40
# text_file_analyzer.py
# A simple text file content analyzer using Bottle framework

from bottle import Bottle, run, request, response, template
import os
import re
from collections import Counter
from typing import List

# Define the Bottle app
app = Bottle()

# Define the route for uploading and analyzing the text file
@app.route('/upload', method='POST')
def upload_file():
    # Check if a file was uploaded
    if 'file' not in request.files:
        return template('upload_form')
    
    file = request.files['file']
    if not file.filename.endswith('.txt'):
        return template('upload_failure', error='Only text files are allowed.')
    
    # Save the uploaded file to the server
    file_path = os.path.join('uploads', file.filename)
    file.save(file_path)
    
    # Analyze the file content
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return analyze_content(content)
    except Exception as e:
        return template('upload_failure', error=str(e))

# Function to analyze the content of the text file
def analyze_content(content: str) -> dict:
    """
    Analyze the content of the text file and return a dictionary
    containing the word count and the most common words.
    
    Args:
    content (str): The content of the text file.
    
    Returns:
    dict: A dictionary containing the word count and the most common words.
    """
    # Use regular expression to split the content into words
    words = re.findall(r'\b\w+\b', content.lower())
    
    # Count the occurrences of each word
    word_count = Counter(words)
    
    # Get the most common words (up to 5 words)
    most_common_words = word_count.most_common(5)
    
    return {
        'total_words': sum(word_count.values()),
        'most_common_words': most_common_words
    }

# Start the Bottle server
if __name__ == '__main__':
    run(app, host='localhost', port=8080)