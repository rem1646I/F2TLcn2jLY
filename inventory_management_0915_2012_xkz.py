# 代码生成时间: 2025-09-15 20:12:54
# inventory_management.py
# A simple inventory management system using Bottle framework.

from bottle import route, run, request, response
import json
from collections import defaultdict

# In-memory inventory storage.
# In a real-world application, this would be replaced with a database.
inventory = defaultdict(list)

# Helper function to parse JSON from request body.
def parse_json(request):
    try:
        return json.loads(request.body.read().decode('utf-8'))
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON format.")

# Route to retrieve items from inventory.
@route('/inventory/<item_id:int>', method='GET')
def get_item(item_id):
    response.content_type = 'application/json'
    items = inventory[item_id]
    if not items:
        return json.dumps({'error': 'Item not found.'})
    return json.dumps({'item_id': item_id, 'items': items})

# Route to add items to inventory.
@route('/inventory', method='POST')
def add_item():
    try:
        data = parse_json(request)
        item_id = data['item_id']
        quantity = data['quantity']
        if quantity <= 0:
            return json.dumps({'error': 'Quantity must be positive.'})
        inventory[item_id].append({'quantity': quantity})
        return json.dumps({'success': f'Added {quantity} units of item {item_id}.'})
    except ValueError as e:
        return json.dumps({'error': str(e)}), 400
    except KeyError as e:
        return json.dumps({'error': f'Missing key: {e}'}), 400

# Route to update the quantity of an item in the inventory.
@route('/inventory/<item_id:int>', method='PUT')
def update_item(item_id):
    try:
        data = parse_json(request)
        quantity = data.get('quantity', 0)
        if quantity <= 0:
            return json.dumps({'error': 'Quantity must be positive.'})
        inventory[item_id] = [{'quantity': quantity}]
        return json.dumps({'success': f'Updated item {item_id} to {quantity} units.'})
    except ValueError as e:
        return json.dumps({'error': str(e)}), 400
    except KeyError as e:
        return json.dumps({'error': f'Missing key: {e}'}), 400

# Route to remove an item from the inventory.
@route('/inventory/<item_id:int>', method='DELETE')
def delete_item(item_id):
    if item_id not in inventory:
        return json.dumps({'error': 'Item not found.'})
    del inventory[item_id]
    return json.dumps({'success': f'Deleted item {item_id}.'})

# Run the application.
# In production, the server should be run with a WSGI server like Gunicorn or uWSGI.
if __name__ == '__main__':
    run(host='localhost', port=8080, debug=True)