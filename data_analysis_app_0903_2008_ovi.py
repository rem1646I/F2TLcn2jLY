# 代码生成时间: 2025-09-03 20:08:36
# 数据分析器应用
# 使用Bottle框架创建一个简单的API服务
# 用于统计和分析数据

from bottle import route, run, request, response
import json
import statistics

# 数据分析器类
class DataAnalyzer:
    def __init__(self):
        # 初始化分析器
        self.data = []

    def add_data(self, new_data):
        # 添加数据
        if isinstance(new_data, (int, float)):
            self.data.append(new_data)
        else:
            raise ValueError("Invalid data type. Expected int or float.")

    def calculate_mean(self):
        # 计算平均值
        if not self.data:
            raise ValueError("No data available.")
        return statistics.mean(self.data)

    def calculate_median(self):
        # 计算中位数
        if not self.data:
            raise ValueError("No data available.")
        return statistics.median(self.data)

    def calculate_mode(self):
        # 计算众数
        try:
            return statistics.mode(self.data)
        except statistics.StatisticsError:
            return "No unique mode found."

# 创建数据分析器实例
analyzer = DataAnalyzer()

# API端点 - 添加数据
@route('/add', method='POST')
def add_data():
    # 从请求中获取JSON数据
    data = request.json
    try:
        analyzer.add_data(data['value'])
        response.status = 201
        return {"message": "Data added successfully."}
    except ValueError as e:
        response.status = 400
        return {"error": str(e)}

# API端点 - 计算平均值
@route('/mean', method='GET')
def calculate_mean():
    try:
        mean = analyzer.calculate_mean()
        return {"mean": mean}
    except ValueError as e:
        response.status = 400
        return {"error": str(e)}

# API端点 - 计算中位数
@route('/median', method='GET')
def calculate_median():
    try:
        median = analyzer.calculate_median()
        return {"median": median}
    except ValueError as e:
        response.status = 400
        return {"error": str(e)}

# API端点 - 计算众数
@route('/mode', method='GET')
def calculate_mode():
    mode = analyzer.calculate_mode()
    return {"mode": mode}

# 启动应用
if __name__ == '__main__':
    run(host='localhost', port=8080, debug=True)