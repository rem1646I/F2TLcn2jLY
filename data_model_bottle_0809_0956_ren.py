# 代码生成时间: 2025-08-09 09:56:13
from bottle import Bottle, run, request, response
from bottle.ext import sqlalchemy
import sqlalchemy as sa
from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

# 数据库连接配置
DATABASE_URI = 'sqlite:///:memory:'

# 创建数据库引擎
engine = create_engine(DATABASE_URI)

# 为ORM会话创建类
Base = declarative_base()

# 数据模型
class UserModel(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)

    # 构造函数
    def __init__(self, name, email):
        self.name = name
        self.email = email

    # 文档字符串
    """User data model."""

# 创建表
Base.metadata.create_all(engine)

# 创建会话
Session = sessionmaker(bind=engine)

# 初始化Bottle应用
app = Bottle()

# SQLAlchemy插件
sa_plugin = sqlalchemy.Plugin(engine)
app.install(sa_plugin)

# 获取所有用户
@app.route('/users', method='GET')
def get_users():
    session = Session()
    try:
        users = session.query(UserModel).all()
        return {'users': [{'name': user.name, 'email': user.email} for user in users]}
    except Exception as e:
        response.status = 500
        return {'error': str(e)}
    finally:
        session.close()

# 添加新用户
@app.route('/users', method='POST')
def add_user():
    session = Session()
    try:
        data = request.json
        user = UserModel(name=data['name'], email=data['email'])
        session.add(user)
        session.commit()
        response.status = 201
        return {'id': user.id, 'name': user.name, 'email': user.email}
    except Exception as e:
        response.status = 400
        return {'error': str(e)}
    finally:
        session.close()

# 运行应用
if __name__ == '__main__':
    run(app, host='localhost', port=8080)
