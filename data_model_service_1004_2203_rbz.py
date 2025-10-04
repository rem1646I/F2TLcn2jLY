# 代码生成时间: 2025-10-04 22:03:05
from bottle import Bottle, run, request, response, HTTPError
from bottle.ext import sqlalchemy
import os

# 数据库配置
SQLALCHEMY_DATABASE_URI = 'sqlite:///data_model.db'
# 创建Bottle应用
app = Bottle()

# 设置数据库
plugin = sqlalchemy.Plugin(SQLALCHEMY_DATABASE_URI)
app.install(plugin)

# 数据模型
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)

    def __repr__(self):
        return '<User(name={self.name}, email={self.email})>'.format(self=self)

# 数据库初始化
def init_db():
    """初始化数据库，创建表"""
    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    Base.metadata.create_all(engine)

# 路由和视图
@app.route('/users', method='GET')
def get_users():
    """获取所有用户信息"""
    session = Session()
    users = session.query(User).all()
    return {'users': [{'name': user.name, 'email': user.email} for user in users]}

@app.route('/users', method='POST')
def add_user():
    """添加新用户"""
    try:
        data = request.json
        name = data.get('name')
        email = data.get('email')
        if not name or not email:
            raise HTTPError(400, 'Missing name or email')
        new_user = User(name=name, email=email)
        session = Session()
        session.add(new_user)
        session.commit()
        response.status = 201
        return {'id': new_user.id, 'name': new_user.name, 'email': new_user.email}
    except Exception as e:
        raise HTTPError(500, 'Error adding user: {}'.format(e))

@app.route('/users/<user_id:int>', method='GET')
def get_user(user_id):
    """获取指定用户信息"""
    session = Session()
    user = session.query(User).filter_by(id=user_id).first()
    if user:
        return {'name': user.name, 'email': user.email}
    else:
        raise HTTPError(404, 'User not found')

@app.route('/users/<user_id:int>', method='PUT')
def update_user(user_id):
    """更新指定用户信息"""
    try:
        data = request.json
        name = data.get('name')
        email = data.get('email')
        session = Session()
        user = session.query(User).filter_by(id=user_id).first()
        if user:
            user.name = name
            user.email = email
            session.commit()
            return {'id': user.id, 'name': user.name, 'email': user.email}
        else:
            raise HTTPError(404, 'User not found')
    except Exception as e:
        raise HTTPError(500, 'Error updating user: {}'.format(e))

@app.route('/users/<user_id:int>', method='DELETE')
def delete_user(user_id):
    """删除指定用户信息"""
    session = Session()
    user = session.query(User).filter_by(id=user_id).first()
    if user:
        session.delete(user)
        session.commit()
        return {'message': 'User deleted'}
    else:
        raise HTTPError(404, 'User not found')

# 运行应用
if __name__ == '__main__':
    init_db()
    run(app, host='localhost', port=8080, debug=True)