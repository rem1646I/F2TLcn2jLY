# 代码生成时间: 2025-09-13 23:09:20
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
消息通知系统
"""

import bottle

# 初始化Bottle应用
app = bottle.Bottle()

# 假设的消息存储列表
messages = []

# 路由：发送消息
@app.route("/send", method="POST")
def send_message():
    """
    发送消息到消息存储列表
    """
    try:
        # 从请求体中获取JSON数据
        data = bottle.request.json
        if not data or not 'message' in data:
            bottle.abort(400, "Missing 'message' in request body")
        
        # 将消息添加到列表中
        messages.append(data['message'])
        
        # 返回成功响应
        return {"status": "success", "message": "Message sent successfully"}
    except Exception as e:
        # 错误处理
        return {"status": "error", "message": str(e)}

# 路由：获取消息列表
@app.route("/messages", method="GET")
def get_messages():
    """
    获取所有消息
    """
    return {"messages": messages}

# 路由：删除所有消息
@app.route("/clear", method="DELETE")
def clear_messages():
    """
    清除所有消息
    """
    global messages
    messages = []
    return {"status": "success", "message": "Messages cleared successfully"}

if __name__ == "__main__":
    # 运行应用
    bottle.run(app, host="localhost", port=8080)