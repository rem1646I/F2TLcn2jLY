# 代码生成时间: 2025-09-10 18:00:29
from bottle import route, run, request, response
import re
import json

# Define a function to parse the log file
def parse_log_file(log_content):
    # Define a regex pattern for log entries
    log_pattern = r"(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)"
    # Find all matches in the log content
    matches = re.findall(log_pattern, log_content)
    # Return the matches as a list of dictionaries
    return [dict(zip(['timestamp', 'ip', 'method', 'endpoint', 'status'], match)) for match in matches]

# Define a route to handle API requests
@route('/parse', method='POST')
def parse_log():
    # Check if the request contains a file
    if 'file' not in request.files:
        response.status = 400
        return json.dumps({'error': 'No file part in the request'})

    # Get the uploaded file
    file = request.files['file']

    # Check if the file is not empty
    if file.filename == '':
        response.status = 400
        return json.dumps({'error': 'No file selected for uploading'})

    # Check if the file is a text file
    if not file.filename.endswith('.txt'):
        response.status = 400
        return json.dumps({'error': 'Invalid file type. Only .txt files are allowed.'})

    # Read the file content
    log_content = file.read().decode('utf-8')

    # Parse the log file
    parsed_data = parse_log_file(log_content)

    # Return the parsed data as JSON
    return json.dumps(parsed_data, indent=4)

# Run the Bottle application
if __name__ == '__main__':
    run(host='localhost', port=8080, debug=True)