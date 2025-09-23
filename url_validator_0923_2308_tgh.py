# 代码生成时间: 2025-09-23 23:08:38
# url_validator.py
# This script uses the Bottle framework to create a simple web application that validates the validity of a URL.

from bottle import route, run, request, HTTPError
from urllib.parse import urlparse
import re

"""
A simple Bottle web application that validates the effectiveness of a URL.
"""


@route('/validate-url', method='GET')
def validate_url():
    """
    A route to handle GET requests and validate the URL.
    """
    url = request.query.url
    if not url:
        raise HTTPError(400, 'URL parameter is missing')
    
    # Check if the URL is valid
    if is_valid_url(url):
        return {'status': 'Valid URL'}
    else:
        return {'status': 'Invalid URL'}


def is_valid_url(url):
    """
    Validates the URL using a regular expression.
    """
    regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+'
        r'(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'localhost|' # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|' # ...or ipv4
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)' # ...or ipv6
        r'(?::[0-9]{1,5})?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, url) is not None


def main():
    """
    The main function that starts the Bottle server.
    """
    run(host='localhost', port=8080, debug=True)

if __name__ == '__main__':
    main()