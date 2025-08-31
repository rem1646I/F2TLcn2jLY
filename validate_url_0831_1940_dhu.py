# 代码生成时间: 2025-08-31 19:40:25
from urllib.parse import urlparse
from bottle import route, run, request, response
import requests

# Function to validate a URL
# It checks if the URL is well-formed and reachable
def is_valid_url(url):
    try:
        result = urlparse(url)
        if all([result.scheme, result.netloc]):
            response = requests.head(url, allow_redirects=True, timeout=5)
            return response.status_code == 200
        return False
    except:
        return False

# Bottle route for validating a URL
@route('/validate_url/<url:path>')
def validate_url(url):
    # Validate the URL
    is_valid = is_valid_url(url)
    # Prepare the response
    if is_valid:
# 扩展功能模块
        message = f"The URL {url} is valid and reachable."
        response.status = 200
    else:
        message = f"The URL {url} is invalid or unreachable."
        response.status = 400
    # Return the result as JSON
    return {"url": url, "is_valid": is_valid, "message": message}

# Start the Bottle server on port 8080
if __name__ == '__main__':
    run(host='localhost', port=8080)