# 代码生成时间: 2025-10-08 02:17:22
# -*- coding: utf-8 -*-

"""
Promotion Engine using Python and Bottle framework.
This engine handles promotional activities.
"""

from bottle import Bottle, request, response, run
import json

# Initialize Bottle app
app = Bottle()

# Define a dictionary to store promotions
promotions = {
    "promo1": {"discount": 20, "description": "20% off on orders over $100"},
    "promo2": {"discount": 10, "description": "10% off on orders over $50"},
    "promo3": {"discount": 5, "description": "5% off on all orders"},
}


# Route for getting all promotions
@app.route("/promotions", method="GET")
def get_promotions():
    """
    Returns a list of all promotions.
    """
    return json.dumps(promotions)


# Route for applying a specific promotion
@app.route("/promotions/<promo_code>", method="POST")
def apply_promotion(promo_code):
    """
    Applies a promotion to the order.
    Expects JSON payload with order details.
    """
    try:
        order_data = request.json
        if promo_code not in promotions:
            response.status = 404
            return json.dumps({"error": "Promotion code not found"})

        promotion = promotions[promo_code]
        order_total = order_data.get("total", 0)
        discount = (order_total * promotion["discount"]) / 100
        new_total = order_total - discount
        return json.dumps({"new_total": new_total, "discount": discount})
    except json.JSONDecodeError:
        response.status = 400
        return json.dumps({"error": "Invalid JSON payload"})
    except KeyError as e:
        response.status = 400
        return json.dumps({"error": f"Missing order detail: {e}"})
    except Exception as e:
        response.status = 500
        return json.dumps({"error": f"Internal server error: {e}"})


# Start the Bottle server
if __name__ == "__main__":
    run(app, host="localhost", port=8080, debug=True)