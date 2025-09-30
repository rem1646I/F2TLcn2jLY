# 代码生成时间: 2025-09-30 20:11:50
#!/usr/bin/env python

"""会员积分系统使用BOTTLE框架实现"""

from bottle import route, run, request, response, HTTPError
import json

# 会员积分系统数据库模拟
class PointsSystem:
    def __init__(self):
        self.points = {}

    def add_member(self, member_id):
        """添加会员"""
        if member_id in self.points:
            raise HTTPError(400, 'Member already exists')
        self.points[member_id] = 0

    def get_points(self, member_id):
        """获取会员积分"""
        if member_id not in self.points:
            raise HTTPError(404, 'Member not found')
        return self.points[member_id]

    def add_points(self, member_id, points):
        """增加会员积分"""
        if member_id not in self.points:
            raise HTTPError(404, 'Member not found')
        if points < 0:
            raise HTTPError(400, 'Points cannot be negative')
        self.points[member_id] += points

# 实例化会员积分系统
points_system = PointsSystem()

# 路由：添加会员
@route('/members', method='POST')
def add_member():
    data = request.json
    member_id = data.get('member_id')
    if not member_id:
        raise HTTPError(400, 'Member ID is required')
    points_system.add_member(member_id)
    response.status = 201
    return json.dumps({'message': 'Member added successfully'})

# 路由：获取会员积分
@route('/members/<member_id:int>/points', method='GET')
def get_points(member_id):
    try:
        points = points_system.get_points(member_id)
        return json.dumps({'member_id': member_id, 'points': points})
    except HTTPError as e:
        response.status = e.status_code
        return json.dumps({'error': str(e)})

# 路由：增加会员积分
@route('/members/<member_id:int>/points', method='PUT')
def add_points(member_id):
    data = request.json
    points = data.get('points')
    if not points or points < 0:
        raise HTTPError(400, 'Points must be positive')
    points_system.add_points(member_id, points)
    return json.dumps({'message': 'Points added successfully'})

# 运行服务器
if __name__ == '__main__':
    run(host='localhost', port=8080)