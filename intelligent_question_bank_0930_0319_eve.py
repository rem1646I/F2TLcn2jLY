# 代码生成时间: 2025-09-30 03:19:25
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Intelligent Question Bank System
This simple web application provides a question bank system that allows
users to view questions and answers, add new questions, and get
random questions with answers.
"""

from bottle import Bottle, request, run, template, redirect

# Initialize the Bottle application
app = Bottle()

# Sample database of questions
# In a real-world application, this would be replaced with a database
questions = [
    {'id': 1, 'question': 'What is the capital of France?', 'answer': 'Paris'},
    {'id': 2, 'question': 'What is the capital of Japan?', 'answer': 'Tokyo'}
]

@app.route('/questions')
def list_questions():
    """
    Returns a list of all questions in the question bank.
    """
    return template('questions', questions=questions)

@app.route('/questions/add', method='POST')
def add_question():
    """
    Adds a new question to the question bank.
    """
    try:
        question = request.forms.get('question')
        answer = request.forms.get('answer')
        questions.append({'id': len(questions) + 1, 'question': question, 'answer': answer})
        return redirect('/questions')
    except Exception as e:
        return template('error', error=str(e))

@app.route('/questions/random')
def random_question():
    """
    Returns a random question with its answer.
    """
    import random
    return template('random_question', question=random.choice(questions))

@app.error(404)
def error_404(error):
    """
    Error handler for 404 Not Found HTTP errors.
    """
    return template('error_page', error=str(error))

if __name__ == '__main__':
    # Run the application
    run(app, host='localhost', port=8080)
