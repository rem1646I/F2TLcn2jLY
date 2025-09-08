# 代码生成时间: 2025-09-08 23:20:59
from bottle import route, run, request, response

"""
A simple Bottle web application that provides an API endpoint to perform sorting algorithms.
"""


# Define the sorting algorithms
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr


def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i-1
        while j >= 0 and key < arr[j]:
            arr[j+1] = arr[j]
            j -= 1
        arr[j+1] = key
    return arr


def selection_sort(arr):
    for i in range(len(arr)):
        min_idx = i
        for j in range(i+1, len(arr)):
            if arr[min_idx] > arr[j]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr


# Define the API endpoint
@route('/sort', method='POST')
def sort_numbers():
    try:
        # Get the list of numbers from the request body
        numbers = request.json.get('numbers')

        # Validate the input
        if not numbers or not all(isinstance(num, (int, float)) for num in numbers):
            response.status = 400
            return {'error': 'Invalid input. Please provide a list of numbers.'}

        # Perform the sorting algorithm
        sorted_numbers = insertion_sort(numbers)  # Change the sorting algorithm as needed

        # Return the sorted list of numbers
        return {'sorted_numbers': sorted_numbers}
    except Exception as e:
        # Handle any unexpected errors
        response.status = 500
        return {'error': str(e)}


# Run the application
if __name__ == '__main__':
    run(host='localhost', port=8080, debug=True)