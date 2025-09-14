# 代码生成时间: 2025-09-14 18:57:23
from bottle import route, run, request, response
# NOTE: 重要实现细节
from threading import Lock
import json
# 扩展功能模块

# 全局库存字典
inventory = {}
# 添加错误处理
# 线程锁，确保线程安全
lock = Lock()

# 初始化库存
def init_inventory():
    inventory["items"] = {}
# 添加错误处理
    inventory["items"]["1"] = {"name": "Item 1", "quantity": 100, "price": 10.99}
    inventory["items"]["2"] = {"name": "Item 2", "quantity": 200, "price": 5.50}

# 获取库存项
@route("/item/<item_id:int>")
def get_item(item_id):
    with lock:
        item = inventory["items"].get(str(item_id))
# 扩展功能模块
        if item:
# NOTE: 重要实现细节
            return json.dumps(item)
        else:
# 优化算法效率
            response.status = 404
            return json.dumps({"error": "Item not found"})

# 更新库存项
@route("/item/<item_id:int>", method='PUT')
def update_item(item_id):
    data = request.json
    with lock:
        if str(item_id) in inventory["items"]:
            inventory["items"][str(item_id)].update(data)
            return json.dumps(inventory["items"][str(item_id)])
        else:
            response.status = 404
            return json.dumps({"error": "Item not found"})

# 添加新库存项
# 扩展功能模块
@route("/item", method='POST')
def add_item():
# FIXME: 处理边界情况
    data = request.json
    with lock:
        if "name" in data and "quantity" in data and "price" in data:
            new_id = max([int(k) for k in inventory["items"].keys()] + [0]) + 1
            inventory["items"][str(new_id)] = data
            return json.dumps(inventory["items"][str(new_id)])
        else:
            response.status = 400
            return json.dumps({"error": "Missing required fields"})

# 删除库存项
@route("/item/<item_id:int>", method='DELETE')
def delete_item(item_id):
    with lock:
        if str(item_id) in inventory["items"]:
            del inventory["items"][str(item_id)]
            return json.dumps({"message": "Item deleted"})
        else:
            response.status = 404
            return json.dumps({"error": "Item not found"})

# 初始化库存
init_inventory()
# TODO: 优化性能

# 运行服务器
# NOTE: 重要实现细节
run(host='localhost', port=8080)
