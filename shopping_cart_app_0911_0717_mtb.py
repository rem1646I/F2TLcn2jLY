# 代码生成时间: 2025-09-11 07:17:59
from bottle import route, run, request, response, template

# Global dictionary to store the shopping cart
shopping_cart = {}

# Route for adding an item to the cart
@route('/add_to_cart/<product_id>')
def add_to_cart(product_id):
    # Get the cart from the global dictionary
    cart = shopping_cart.get(request.get_cookie('cart_id'), {})
    # If the product_id is not in the cart, add it
    if product_id not in cart:
        cart[product_id] = {'quantity': 1, 'added': True}
    # If it is already in the cart, increment the quantity
    else:
        cart[product_id]['quantity'] += 1
    # Update the cart in the global dictionary
    shopping_cart[request.get_cookie('cart_id')] = cart
    response.set_cookie('cart_id', request.get_cookie('cart_id'))
    return f"{product_id} added to cart."

# Route for removing an item from the cart
@route('/remove_from_cart/<product_id>')
def remove_from_cart(product_id):
    cart = shopping_cart.get(request.get_cookie('cart_id'), {})
    if product_id in cart:
        del cart[product_id]
        shopping_cart[request.get_cookie('cart_id')] = cart
        response.set_cookie('cart_id', request.get_cookie('cart_id'))
        return f"{product_id} removed from cart."
    else:
        return f"{product_id} not found in cart."

# Route for viewing the cart
@route('/view_cart')
def view_cart():
    cart = shopping_cart.get(request.get_cookie('cart_id'), {})
    return template('cart_template', cart=cart)

# Route for clearing the cart
@route('/clear_cart')
def clear_cart():
    cart_id = request.get_cookie('cart_id')
    if cart_id in shopping_cart:
        del shopping_cart[cart_id]
        response.set_cookie('cart_id', '', path='/', max_age=0)  # Clear the cookie
        return 'Cart cleared.'
    else:
        return 'No cart found.'

# Route for initializing a new cart
@route('/new_cart')
def new_cart():
    new_cart_id = str(len(shopping_cart) + 1)  # Simple way to generate a unique cart id
    shopping_cart[new_cart_id] = {}
    response.set_cookie('cart_id', new_cart_id)
    return f'New cart created with ID: {new_cart_id}'

# HTML template for the cart
@route('/cart_template')
def cart_template(cart):
    return f"""
    <html><body>
        <h2>Your Cart ({len(cart)} items)</h2>
        <ul>
            % for product_id, details in cart.items():
                <li>{{product_id}}: {{details['quantity']}} - <a href='/remove_from_cart/{{product_id}}'>Remove</a></li>
            % end
        </ul>
    </body></html>
    """

# Run the application on localhost port 8080
run(host='localhost', port=8080)