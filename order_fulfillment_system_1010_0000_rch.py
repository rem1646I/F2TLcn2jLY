# 代码生成时间: 2025-10-10 00:00:26
from bottle import route, run, request, response, HTTPError

# 模拟数据库中的订单数据
ORDERS = {
    "1": {"item": "Laptop", "status": "pending"},
    "2": {"item": "Smartphone", "status": "fulfilled"},
    "3": {"item": "Tablet", "status": "pending"}
}

# 添加一个新的订单
@route('/order', method='POST')
def create_order():
    try:
        order_data = request.json
        order_id = max(ORDERS.keys()) + 1  # 生成新的订单ID
        ORDERS[str(order_id)] = {
            "item": order_data["item"],
            "status": "pending"
        }
        response.status = 201
        return {"message": "Order created", "order_id": order_id}
    except KeyError:
        raise HTTPError(400, "Missing order item")
    except Exception as e:
        raise HTTPError(500, str(e))

# 获取订单信息
@route('/order/<order_id:int>', method='GET')
def get_order(order_id):
    try:
        order = ORDERS.get(order_id)
        if order is None:
            raise KeyError
        return order
    except KeyError:
        raise HTTPError(404, "Order not found")
    except Exception as e:
        raise HTTPError(500, str(e))

# 更新订单状态
@route('/order/<order_id:int>', method='PUT')
def update_order(order_id):
    try:
        order_data = request.json
        order = ORDERS.get(order_id)
        if order is None:
            raise KeyError
        order["status"] = order_data["status"]
        return {"message": "Order updated", "order": order}
    except KeyError:
        raise HTTPError(404, "Order not found")
    except Exception as e:
        raise HTTPError(500, str(e))

# 删除订单
@route('/order/<order_id:int>', method='DELETE')
def delete_order(order_id):
    try:
        if ORDERS.pop(order_id, None) is None:
            raise KeyError
        return {"message": "Order deleted"}
    except KeyError:
        raise HTTPError(404, "Order not found")
    except Exception as e:
        raise HTTPError(500, str(e))

# 运行Bottle服务器
if __name__ == '__main__':
    run(host='localhost', port=8080)