# 代码生成时间: 2025-10-02 19:29:42
# online_exam_system.py
#
# 一个简单的在线考试系统，使用Bottle框架实现。

import bottle
from bottle.ext import jinja2
import json

# 设置Bottle的模板引擎为Jinja2
bottle.TEMPLATES.clear()
bottle.TEMPLATES['jinja2'] = jinja2.Jinja2()

# 考试题库
EXAM_QUESTIONS = [
    {
        "question": "What is the capital of France?",
        "options": ["Paris", "London", "Berlin", "Madrid"],
        "answer": "Paris"
    },
    # 可以根据需要添加更多题目
]

# 学生答案存储
student_answers = {}

# 路由：显示考试页面
@bottle.route('/')
def exam_page():
    return bottle.template('exam', questions=EXAM_QUESTIONS)

# 路由：提交答案
@bottle.route('/submit', method='POST')
def submit_answers():
    try:
        # 获取学生提交的答案并存储
        student_answers[request.forms.get('student_id')] = request.forms.get('answers')
        
        # 返回成绩页面
        return bottle.template('results', scores=calculate_scores())
    except Exception as e:
        # 错误处理
        return str(e)

# 计算分数
def calculate_scores():
    scores = {}
    for student_id, answers in student_answers.items():
        score = 0
        for i, student_answer in enumerate(answers):
            if student_answer == EXAM_QUESTIONS[i]['answer']:
                score += 1
        scores[student_id] = score
    return scores

# 设置静态文件目录
@bottle.route('/static/<filename:path>')
def send_js(filename):
    return bottle.static_file(filename, root='static')

if __name__ == '__main__':
    bottle.run(host='localhost', port=8080, debug=True)
