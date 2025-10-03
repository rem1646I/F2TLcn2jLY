# 代码生成时间: 2025-10-03 20:03:14
#!/usr/bin/env python

# 引入Bottle框架库
from bottle import Bottle, request, run, static_file, redirect, template, HTTPError
from datetime import datetime
import json

# 定义任务分配系统的主类
class TaskAssignmentSystem:
    def __init__(self):
        # 初始化Bottle应用
        self.app = Bottle()
        # 初始化任务存储列表
        self.tasks = []

    # 获取所有任务
    def get_tasks(self):
        return {
            "tasks": self.tasks
        }

    # 添加新任务
    def add_task(self):
        try:
            # 从请求体中获取任务信息
            content = request.json
            new_task = {
                "id": len(self.tasks) + 1,
                "description": content.get("description"),
                "assigned_to": content.get("assigned_to"),
                "due_date": content.get("due_date"),
                "status": "pending"
            }
            # 将新任务添加到任务列表
            self.tasks.append(new_task)
            return new_task
        except Exception as e:
            # 处理异常
            return {"error": str(e)}

    # 更新任务状态
    def update_task_status(self, task_id):
        try:
            # 从请求体中获取状态信息
            content = request.json
            status = content.get("status")
            # 查找任务并更新状态
            for task in self.tasks:
                if task["id"] == task_id:
                    task["status"] = status
                    return task
            raise ValueError("Task not found")
        except Exception as e:
            # 处理异常
            return {"error": str(e)}

    # 设置Bottle路由
    def setup_routes(self):
        # 获取所有任务的路由
        @self.app.route("/tasks", method="GET")
        def get_all_tasks():
            return json.dumps(self.get_tasks())

        # 添加任务的路由
        @self.app.route("/tasks", method="POST")
        def create_task():
            return json.dumps(self.add_task())

        # 更新任务状态的路由
        @self.app.route("/tasks/<task_id:int>/status", method="PUT")
        def update_task(task_id):
            return json.dumps(self.update_task_status(task_id))

# 实例化任务分配系统
task_system = TaskAssignmentSystem()

# 调用setup_routes方法设置路由
task_system.setup_routes()

# 运行Bottle应用
if __name__ == "__main__":
    run(task_system.app, host="localhost", port=8080)