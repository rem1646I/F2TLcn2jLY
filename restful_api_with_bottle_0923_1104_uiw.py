# 代码生成时间: 2025-09-23 11:04:10
from bottle import route, run, request, response, error

# 数据存储模拟，实际应用中应使用数据库
items = []

# 获取所有项目
@route('/api/items')
def get_items():
    return items

# 获取单个项目
@route('/api/items/<item_id:int>')
def get_item(item_id):
    item = next((item for item in items if item['id'] == item_id), None)
    if item:
        return item
    else:
        response.status = 404
        return {"error": "Item not found"}

# 创建新项目
@route('/api/items', method='POST')
def create_item():
    try:
        item = request.json
        items.append(item)
        return item
    except ValueError:
        response.status = 400
        return {"error": "Invalid JSON"}

# 更新项目
@route('/api/items/<item_id:int>', method='PUT')
def update_item(item_id):
    try:
        item = request.json
        item['id'] = item_id
        for i, _item in enumerate(items):
            if _item['id'] == item_id:
                items[i] = item
                return item
        else:
            response.status = 404
            return {"error": "Item not found"}
    except ValueError:
        response.status = 400
        return {"error": "Invalid JSON"}

# 删除项目
@route('/api/items/<item_id:int>', method='DELETE')
def delete_item(item_id):
    global items
    items = [item for item in items if item['id'] != item_id]
    if not any(item['id'] == item_id for item in items):
        return {"result": "Item deleted"}
    else:
        response.status = 404
        return {"error": "Item not found"}

# 错误处理
@error(404)
def error404(error):
    return {"error": "Resource not found"}, 404

# 错误处理
@error(400)
def error400(error):
    return {"error": "Bad Request"}, 400

# 启动服务
if __name__ == '__main__':
    run(host='localhost', port=8080, debug=True)