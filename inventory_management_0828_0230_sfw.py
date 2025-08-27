# 代码生成时间: 2025-08-28 02:30:03
#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 引入Bottle框架
from bottle import route, run, request, response, HTTPError

# 库存数据模拟
inventory = {
    'item1': {'name': 'Item 1', 'quantity': 10},
    'item2': {'name': 'Item 2', 'quantity': 20},
    'item3': {'name': 'Item 3', 'quantity': 15},
}

# 路由：列出所有库存项
@route('/inventory')
def list_inventory():
    """
    列出所有库存项
    """
    response.content_type = 'application/json'
    return {'inventory': inventory}

# 路由：获取单个库存项
@route('/inventory/<item_id>')
def get_inventory_item(item_id):
    """
    根据ID获取单个库存项
    """
    item = inventory.get(item_id)
    if item:
        response.content_type = 'application/json'
        return item
    else:
        raise HTTPError(404, 'Item not found')

# 路由：添加或更新库存项
@route('/inventory/<item_id>', method='PUT')
def update_inventory_item(item_id):
    """
    添加或更新库存项
    """
    try:
        data = request.json
        if item_id in inventory:
            # 更新库存项
            inventory[item_id]['quantity'] = data['quantity']
        else:
            # 添加新库存项
            inventory[item_id] = data
        response.status = 200
        response.content_type = 'application/json'
        return {'message': 'Item updated'}
    except Exception as e:
        raise HTTPError(400, 'Invalid data', e)

# 路由：删除库存项
@route('/inventory/<item_id>', method='DELETE')
def delete_inventory_item(item_id):
    """
    删除库存项
    """
    try:
        if item_id in inventory:
            del inventory[item_id]
            response.status = 200
            response.content_type = 'application/json'
            return {'message': 'Item deleted'}
        else:
            raise HTTPError(404, 'Item not found')
    except Exception as e:
        raise HTTPError(500, 'Server error', e)

# 运行Bottle服务器
if __name__ == '__main__':
    run(host='localhost', port=8080)
