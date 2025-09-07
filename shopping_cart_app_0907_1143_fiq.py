# 代码生成时间: 2025-09-07 11:43:48
#!/usr/bin/env python

# shopping_cart_app.py
# This script creates a simple shopping cart application using the Bottle framework.

from bottle import route, run, request, response, redirect, HTTPError
from collections import defaultdict

# In-memory shopping cart storage. In a real-world scenario, this would be
# replaced with a database or a persistent storage system.
shopping_cart = defaultdict(list)

# Helper function to update the shopping cart.
def update_cart(item_id, quantity=1, action='add'):
    if action == 'add':
        shopping_cart[item_id].append(quantity)
    elif action == 'remove':
        if shopping_cart[item_id]:
            shopping_cart[item_id].pop(0)
            if not shopping_cart[item_id]:
                del shopping_cart[item_id]
    else:
        raise ValueError("Invalid action. Use 'add' or 'remove'.")

# Route to display the shopping cart.
@route('/shopping-cart')
def show_cart():
    """
    Display the current state of the shopping cart.
    """
    return {"cart": dict(shopping_cart)}

# Route to add an item to the shopping cart.
@route('/add-to-cart/<item_id:int>')
def add_to_cart(item_id):
    """
    Add a specified quantity of an item to the shopping cart.
    """
    try:
        update_cart(item_id)
        redirect('/shopping-cart')
    except ValueError as e:
        raise HTTPError(400, str(e))

# Route to remove an item from the shopping cart.
@route('/remove-from-cart/<item_id:int>')
def remove_from_cart(item_id):
    """
    Remove a specified quantity of an item from the shopping cart.
    """
    try:
        update_cart(item_id, action='remove')
        redirect('/shopping-cart')
    except ValueError as e:
        raise HTTPError(400, str(e))

# Run the Bottle application.
if __name__ == '__main__':
    run(host='localhost', port=8080, debug=True)