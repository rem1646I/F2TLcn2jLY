# 代码生成时间: 2025-08-06 03:26:41
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Interactive Chart Generator using Bottle framework.
This application allows users to generate interactive charts by providing data and chart options.
"""

from bottle import route, run, request, response, template
import json
import os
import sys

# Define the path to store chart files
CHART_DIRECTORY = "charts/"

# Ensure the chart directory exists
if not os.path.exists(CHART_DIRECTORY):
    os.makedirs(CHART_DIRECTORY)

# Define the Bottle routes
@route("/")
def index():
    """
    The index route serves the main page where users can input data and chart options.
    """
    return template("index")

@route("/chart", method="POST")
def generate_chart():
    """
    The chart route handles the POST request to generate an interactive chart.
    It expects a JSON payload with data and chart options.
    """
    try:
        # Get the JSON payload from the request
        payload = request.json
        data = payload.get("data")
        options = payload.get("options")

        # Validate the data and options
        if not data or not options:
            return json_response("Missing data or chart options", status=400)

        # Check if the chart directory is writable
        if not os.access(CHART_DIRECTORY, os.W_OK):
            return json_response("Chart directory is not writable", status=500)

        # Generate the chart filename
        chart_filename = generate_filename()
        chart_path = os.path.join(CHART_DIRECTORY, chart_filename)

        # Save the chart data to the file
        with open(chart_path, "w") as f:
            f.write(json.dumps(payload))

        # Return the chart URL
        return json_response({"chart_url": f"{request.url_root}{chart_filename}"})

    except Exception as e:
        # Handle any exceptions and return an error response
        return json_response(str(e), status=500)

def generate_filename():
    """
    Generate a unique filename for the chart.
    """
    import uuid
    return f"chart-{uuid.uuid4()}.json"

def json_response(message, status=200):
    """
    Return a JSON response with the given message and status code.
    """
    response.content_type = "application/json"
    return json.dumps({"message": message}, indent=4) + "
"

if __name__ == "__main__":
    # Run the Bottle server
    run(host="localhost", port=8080, debug=True)
