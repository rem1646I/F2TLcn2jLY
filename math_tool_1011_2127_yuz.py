# 代码生成时间: 2025-10-11 21:27:45
from bottle import route, run, request, response

"""
Math Tool: A simple web application using Bottle framework to provide basic math operations.
"""


# Define the supported operations
SUPPORTED_OPERATIONS = {'+': 'add', '-': 'subtract', '*': 'multiply', '/': 'divide'}


# Define the math operations
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b

# Define a function to perform the operations
def perform_operation(operation, a, b):
    try:
        return globals()[SUPPORTED_OPERATIONS[operation]](a, b)
    except KeyError:
        raise ValueError(f"Unsupported operation: {operation}")
    except ValueError as e:
        raise ValueError(str(e))

# Define the route for the math tool
@route('/math/<operation>/<a:float>/<b:float>')
def math_tool(operation, a, b):
    try:
        result = perform_operation(operation, a, b)
        return {"result": result}
    except ValueError as e:
        response.status = 400
        return {"error": str(e)}

# Run the application
if __name__ == '__main__':
    run(host='localhost', port=8080)
