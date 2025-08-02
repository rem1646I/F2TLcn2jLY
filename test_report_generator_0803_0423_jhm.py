# 代码生成时间: 2025-08-03 04:23:32
# test_report_generator.py
# This is a Bottle-powered web application that generates test reports.

from bottle import Bottle, response, static_file, run
import os
import json
import datetime

# Initialize Bottle app
app = Bottle()

# Folder to store test reports
REPORTS_FOLDER = 'reports'

# Ensure reports folder exists
if not os.path.exists(REPORTS_FOLDER):
    os.makedirs(REPORTS_FOLDER)

# Route to serve the test report generator page
@app.route('/')
def index():
    """Serve the test report generator HTML page."""
    return static_file('index.html', root='./')

# Route to handle the POST request for generating test reports
@app.route('/generate', method='POST')
def generate_report():
    """Generate a test report based on user input."""
    try:
        # Get data from POST request
        data = request.json
        
        # Validate data
        if 'test_name' not in data or 'results' not in data:
            response.status = 400
            return json.dumps({'error': 'Missing test data'})
        
        # Extract test information
        test_name = data['test_name']
        results = data['results']
        
        # Create a report file name and path
        report_filename = f'{test_name}_{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}.html'
        report_path = os.path.join(REPORTS_FOLDER, report_filename)
        
        # Generate the test report content
        report_content = f'<h1>{test_name}</h1>\
<ul>\
'
        for result in results:
            report_content += f'<li>Test {result[