# 代码生成时间: 2025-08-31 01:14:28
# random_number_generator.py
# This script is a Bottle web application that provides a random number generator.

from bottle import route, run, request
import random
import json

# Define the route for generating random numbers
@route('/generate_random_number')
def generate_random_number():
    # Get the parameters from the request
    try:
        min_value = int(request.query.min)
        max_value = int(request.query.max)
    except (ValueError, TypeError):
        # Handle invalid or missing parameters
        return json.dumps({'error': 'Invalid or missing parameters. Please provide min and max values.'})
    
    # Generate a random number within the given range
    try:
        random_number = random.randint(min_value, max_value)
    except ValueError:
        # Handle invalid range
        return json.dumps({'error': 'Invalid range. Please ensure min value is less than max value.'})
    
    # Return the generated random number in JSON format
    return json.dumps({'random_number': random_number})

# Run the Bottle application on localhost, port 8080
run(host='localhost', port=8080, debug=True)
