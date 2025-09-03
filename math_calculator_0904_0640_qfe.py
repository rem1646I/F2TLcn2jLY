# 代码生成时间: 2025-09-04 06:40:08
from bottle import route, run, request, response

# 导入所需的库
import math

def add(x, y):
    """Add two numbers."""
    return x + y

def subtract(x, y):
    """Subtract two numbers."""
    return x - y

def multiply(x, y):
    """Multiply two numbers."""
    return x * y

def divide(x, y):
    """Divide two numbers."""
    if y == 0:
        return 'Cannot divide by zero'
    return x / y

def power(x, y):
    """Raise x to the power of y."""
    return x ** y

def square_root(x):
    """Calculate the square root of x."""
    if x < 0:
        return 'Cannot calculate square root of negative number'
    return math.sqrt(x)

# 定义路由和对应的函数
@route('/add/<float:x>/<float:y>')
def add_numbers(x, y):
    return str(add(x, y))

@route('/subtract/<float:x>/<float:y>')
def subtract_numbers(x, y):
    return str(subtract(x, y))

@route('/multiply/<float:x>/<float:y>')
def multiply_numbers(x, y):
    return str(multiply(x, y))

@route('/divide/<float:x>/<float:y>')
def divide_numbers(x, y):
    result = divide(x, y)
    if isinstance(result, str):
        response.status = 400
        return result
    return str(result)

@route('/power/<float:x>/<float:y>')
def power_numbers(x, y):
    return str(power(x, y))

@route('/sqrt/<float:x>')
def square_root_number(x):
    result = square_root(x)
    if isinstance(result, str):
        response.status = 400
        return result
    return str(result)

# 启动Bottle服务
if __name__ == '__main__':
    run(host='localhost', port=8080)