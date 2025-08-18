# 代码生成时间: 2025-08-18 13:40:56
from bottle import Bottle, run, request, response, template

# 定义全局购物车字典
shopping_cart = {}

# 初始化Bottle应用
app = Bottle()

# 路由：添加商品到购物车
@app.route('/add', method='POST')
def add_to_cart():
    product_id = request.forms.get('product_id')
    quantity = int(request.forms.get('quantity', 0))
    if not product_id:
        return template("Error template", error="Product ID is required")
    if product_id in shopping_cart:
        shopping_cart[product_id] += quantity
    else:
        shopping_cart[product_id] = quantity
    return template("Cart template", cart=shopping_cart)

# 路由：从购物车中删除商品
@app.route('/remove', method='POST')
def remove_from_cart():
    product_id = request.forms.get('product_id')
    if not product_id:
        return template("Error template", error="Product ID is required")
    if product_id in shopping_cart:
        del shopping_cart[product_id]
    return template("Cart template", cart=shopping_cart)

# 路由：查看购物车
@app.route('/cart')
def view_cart():
    return template("Cart template", cart=shopping_cart)

# 路由：清空购物车
@app.route('/clear', method='GET')
def clear_cart():
    global shopping_cart
    shopping_cart = {}
    return template("Cart template", cart=shopping_cart)

# 启动Bottle应用
if __name__ == '__main__':
    run(app, host='localhost', port=8080)

# 模板：购物车页面模板
TEMPLATE_CART = """
<!DOCTYPE html>
<html>
<head>
    <title>Shopping Cart</title>
</head>
<body>
    <h1>Your Shopping Cart</h1>
    %for product_id, quantity in cart.items():
        <p>Product ID: {{product_id}}, Quantity: {{quantity}}</p>
    %end
    <a href="/add">Add Product</a>
    <a href="/clear">Clear Cart</a>
</body>
</html>
"""

# 模板：错误页面模板
TEMPLATE_ERROR = """
<!DOCTYPE html>
<html>
<head>
    <title>Error</title>
</head>
<body>
    <h1>Error</h1>
    <p>{{error}}</p>
    <a href="/cart">Back to Cart</a>
</body>
</html>
"""
