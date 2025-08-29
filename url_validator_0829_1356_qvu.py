# 代码生成时间: 2025-08-29 13:56:42
# url_validator.py
# This script uses the Bottle framework to create a simple URL validity check service.

from bottle import route, run, request
from urllib.parse import urlparse
import requests

# Define the base URL for the service
BASE_URL = 'http://localhost:8080/'

# Function to check if the URL is valid
def is_valid_url(url):
    """
    Checks if a given URL is valid.
    Returns True if valid, False otherwise.
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

# Function to fetch the URL content
def fetch_url_content(url):
    """
    Attempts to fetch the content of a given URL.
    Returns the content if successful, or an error message.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        return f'Error fetching URL: {e}'

# Route for validating a URL
@route('/validate_url', method='GET')
def validate_url():
    """
    Bottle route handler for URL validation.
    Returns a JSON response indicating the validity of the URL.
    """
    url_to_check = request.query.url
    if not url_to_check:
        return {'error': 'No URL provided'}

    is_valid = is_valid_url(url_to_check)
    if is_valid:
        content = fetch_url_content(url_to_check)
        return {'valid': True, 'content': content}
    else:
        return {'valid': False}

# Run the Bottle server
if __name__ == '__main__':
    run(host='localhost', port=8080)