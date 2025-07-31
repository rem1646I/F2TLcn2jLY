# 代码生成时间: 2025-07-31 20:42:17
# interactive_chart_generator.py
# This Bottle application serves as an interactive chart generator.

from bottle import route, run, template, request, static_file
import json
import random
import os

# Configuration
PORT = 8080
DATA_DIR = 'data'

# Ensure data directory exists
if not os.path.exists(DATA_DIR): os.makedirs(DATA_DIR)

# Define a route for serving the static files
@route('/static/<filepath:path>')
def server_static(filepath): return static_file(filepath, root='static')

# Define a route for the main page
@route('/')
def index():
    return template('index')

# Define a route to generate and display charts
@route('/generate-chart', method='POST')
def generate_chart():
    try:
        # Get the data from the POST request
        data = request.json
        if not data:
            return {'error': 'No data provided'}

        # Generate a random chart title
        chart_title = f'Chart {random.randint(100, 999)}'

        # Save the data to a file
        file_path = os.path.join(DATA_DIR, chart_title + '.json')
        with open(file_path, 'w') as file:
            json.dump(data, file)

        # Return the chart generation response
        return {'message': 'Chart generated successfully', 'title': chart_title, 'file_path': file_path}
    except Exception as e:
        return {'error': str(e)}

# Define a route to display the chart
@route('/chart/<chart_file:path>')
def display_chart(chart_file):
    chart_file_path = os.path.join(DATA_DIR, chart_file)
    if not os.path.isfile(chart_file_path): return {'error': 'Chart file not found'}

    # Serve the chart file
    return static_file(chart_file_path, root=DATA_DIR)

# Run the Bottle application
if __name__ == '__main__':
    run(host='localhost', port=PORT, debug=True)


# Static template for the main page
TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Interactive Chart Generator</title>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
  <h1>Interactive Chart Generator</h1>
  <div id="chart-container" style="width: 400px; height: 400px; position: relative; margin: auto"></div>
  <script>
    const config = {{config | tojson}}; // Chart configuration passed from the backend
    const ctx = document.getElementById('chart-container').getContext('2d');
    new Chart(ctx, config);
  </script>
</body>
</html>
"""

