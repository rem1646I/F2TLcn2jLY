# 代码生成时间: 2025-08-22 02:19:18
from bottle import route, run, template, request, response
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.resources import CDN
from bokeh.models import ColumnDataSource
import json

"""
Interactive Chart Generator using Python and the Bottle framework.
This application allows users to generate interactive charts based on user input.
"""

# Define the route for the interactive chart generator
@route('/interactive_chart')
def interactive_chart():
    # Get user input data
    user_input = request.query.getall('data')
    if not user_input:
        return template("interactive_chart_generator_error", error="No input data provided.")

    # Parse user input data
    try:
        input_data = [json.loads(data) for data in user_input]
    except json.JSONDecodeError:
        return template("interactive_chart_generator_error", error="Invalid JSON format.")

    # Create a ColumnDataSource from the input data
    source = ColumnDataSource(data=input_data)

    # Create a figure for the chart
    p = figure(title="Interactive Chart", sizing_mode="stretch_width")
    p.line(x="x", y="y", source=source)

    # Embed the chart in the HTML template
    script, div = components(p, CDN)
    return template("interactive_chart_generator_template", script=script, div=div)

# Run the Bottle application
run(host='localhost', port=8080)
