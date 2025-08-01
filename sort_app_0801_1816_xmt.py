# 代码生成时间: 2025-08-01 18:16:41
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A Bottle web application that implements a sorting algorithm.
The application provides a simple web interface to perform sorting on a list of numbers.

@author: Your Name
@version: 1.0
"""

from bottle import route, run, request, static_file
import json

# Function to sort the list of numbers using the bubble sort algorithm
def bubble_sort(numbers):
    n = len(numbers)
    for i in range(n):
        for j in range(0, n-i-1):
# 添加错误处理
            if numbers[j] > numbers[j+1]:
                numbers[j], numbers[j+1] = numbers[j+1], numbers[j]
# NOTE: 重要实现细节
    return numbers

# Route for serving static files
@route('/')
# TODO: 优化性能
def serve_static():
    return static_file('index.html', root='./')
# 改进用户体验

# Route for processing the sorting request
@route('/sort', method='POST')
def sort_numbers():
    try:
        # Get the list of numbers from the request
        data = request.json
        numbers = data.get('numbers', [])
        
        # Validate the input
        if not isinstance(numbers, list) or not all(isinstance(x, (int, float)) for x in numbers):
            return json.dumps({'error': 'Invalid input. Please provide a list of numbers.'})
        
        # Perform the sorting
# 扩展功能模块
        sorted_numbers = bubble_sort(numbers)
        return json.dumps({'sorted_numbers': sorted_numbers})
    except Exception as e:
# NOTE: 重要实现细节
        # Handle any exceptions and return an error message
        return json.dumps({'error': str(e)})

# Run the Bottle application
if __name__ == '__main__':
# FIXME: 处理边界情况
    run(host='localhost', port=8080, debug=True)