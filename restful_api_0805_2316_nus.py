# 代码生成时间: 2025-08-05 23:16:15
from bottle import route, run, request, response, HTTPError

"""
A simple RESTful API using Bottle framework.

This API exposes two endpoints:
- GET /api/items - Retrieves a list of items.
- POST /api/items - Creates a new item.
"""

# In-memory data store
items = []

# Helper function to generate a unique item ID
def generate_id():
    return len(items) + 1

# GET /api/items - Retrieve all items
@route('/api/items', method='GET')
def get_items():
    return {"items": items}

# POST /api/items - Create a new item
@route('/api/items', method='POST')
def create_item():
    try:
        data = request.json
        if not data:
            raise HTTPError(400, 'No data provided')
        if 'name' not in data:
            raise HTTPError(400, 'Missing item name')
        item = {"id": generate_id(), "name": data['name']}
        items.append(item)
        response.status = 201
        return item
    except Exception as e:
        # Generic error handling
        return HTTPError(500, str(e))

# Main function to run the server
def main():
    run(host='localhost', port=8080, debug=True)

if __name__ == '__main__':
    main()
