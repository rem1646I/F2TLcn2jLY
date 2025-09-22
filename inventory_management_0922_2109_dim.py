# 代码生成时间: 2025-09-22 21:09:09
from bottle import route, run, request, response, abort

# Inventory item class
class InventoryItem:
    def __init__(self, item_id, name, quantity):
        self.item_id = item_id
        self.name = name
        self.quantity = quantity

# Inventory class
class Inventory:
    def __init__(self):
        self.items = {}

    def add_item(self, item_id, name, quantity):
        if item_id in self.items:
            raise ValueError(f"Item with ID {item_id} already exists.")
        self.items[item_id] = InventoryItem(item_id, name, quantity)

    def get_item(self, item_id):
        return self.items.get(item_id, None)

    def update_item_quantity(self, item_id, quantity):
        if item_id not in self.items:
            raise ValueError(f"Item with ID {item_id} does not exist.")
        self.items[item_id].quantity = quantity

    def remove_item(self, item_id):
        if item_id not in self.items:
            raise ValueError(f"Item with ID {item_id} does not exist.")
        del self.items[item_id]

# Initialize the inventory
inventory = Inventory()

# API routes
@route('/item', method='POST')
def add_item():
    data = request.json
    try:
        inventory.add_item(data['item_id'], data['name'], data['quantity'])
        response.status = 201
        return {"message": "Item added successfully."}
    except ValueError as e:
        abort(400, e)

@route('/item/:id', method='GET')
def get_item(id):
    item = inventory.get_item(id)
    if item is None:
        abort(404, f"Item with ID {id} not found.")
    return {
        "item_id": item.item_id,
        "name": item.name,
        "quantity": item.quantity
    }

@route('/item/:id', method='PUT')
def update_item(id):
    data = request.json
    item = inventory.get_item(id)
    if item is None:
        abort(404, f"Item with ID {id} not found.")
    try:
        inventory.update_item_quantity(id, data['quantity'])
        return {"message": "Item updated successfully."}
    except ValueError as e:
        abort(400, e)

@route('/item/:id', method='DELETE')
def remove_item(id):
    try:
        inventory.remove_item(id)
        return {"message": "Item removed successfully."}
    except ValueError as e:
        abort(400, e)

# Run the Bottle server
run(host='localhost', port=8080)