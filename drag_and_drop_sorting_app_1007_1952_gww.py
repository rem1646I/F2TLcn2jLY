# 代码生成时间: 2025-10-07 19:52:45
from bottle import route, run, template, static_file

# 定义一个全局列表，用于存储拖拽排序的元素
drag_and_drop_list = []

# 路由：用于返回拖拽排序组件的HTML页面
@route('/')
def index():
    return template('index')

# 路由：用于处理拖拽排序组件的排序请求
@route('/sort', method='POST')
def sort_items():
    global drag_and_drop_list
    # 获取排序后的列表，JSON格式
    sorted_list = request.json.get('list')
    
    # 错误处理：确保接收到的数据是列表，并且列表不为空
    if not isinstance(sorted_list, list) or not sorted_list:
        return {
            'error': 'Invalid input: expected a non-empty list'
        }
    
    # 更新全局拖拽排序列表
    drag_and_drop_list = sorted_list
    
    # 返回成功信息
    return {'status': 'success'}

# 路由：提供静态文件服务
@route('/static/<filename:path>')
def serve_static(filename):
    return static_file(filename, root='./static')

# HTML模板文件，用于拖拽排序组件
index_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Drag and Drop Sorting</title>
    <link rel="stylesheet" href="/static/style.css">
    <script src="/static/sortable.min.js"></script>
</head>
<body>
    <div id="list-container">
        <ol id="drag-and-drop-list">
            % for item in drag_and_drop_list:
            <li class="ui-sortable-handle">{{item}}</li>
            % end
        </ol>
    </div>
    <script>
        var listContainer = document.getElementById('drag-and-drop-list');
        var sortable = Sortable.create(listContainer, {
            onEnd: function (event) {
                // 将排序后的列表发送到服务器
                fetch('/sort', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        list: Array.from(listContainer.children).map(function(child) {
                            return child.textContent;
                        })
                    })
                }).then(function(response) {
                    return response.json();
                }).then(function(data) {
                    if (data.status !== 'success') {
                        alert('Error: ' + data.error);
                    }
                }).catch(function(error) {
                    console.error('Error:', error);
                });
            }
        });
    </script>
</body>
</html>
"""

# 运行Bottle应用
if __name__ == '__main__':
    run(host='localhost', port=8080)
