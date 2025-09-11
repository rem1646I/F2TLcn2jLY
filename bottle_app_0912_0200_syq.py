# 代码生成时间: 2025-09-12 02:00:39
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A simple Bottle application to demonstrate data model and RESTful API design.
"""

from bottle import Bottle, run, request, response, HTTPError
import json

# Initialize the Bottle app
app = Bottle()

# Define our data models as dictionaries, for simplicity
users = [
    {"id": 1, "name": "John Doe", "email": "john@example.com"},
    {"id": 2, "name": "Jane Doe", "email": "jane@example.com"}
]

# Helper function to find a user by ID
def get_user_by_id(user_id):
    for user in users:
        if user['id'] == user_id:
            return user
    return None

# HTTP Error handler for 404 Not Found
@app.error(404)
def error_404(error):
    return json.dumps({'error': 'Resource not found'}), 404, {'ContentType': 'application/json'}

# HTTP Error handler for 500 Internal Server Error
@app.error(500)
def error_500(error):
    return json.dumps({'error': 'Internal server error'}), 500, {'ContentType': 'application/json'}

# Route to get all users
@app.get('/users')
def get_users():
    return json.dumps(users)

# Route to get a single user by ID
@app.get('/users/<user_id:int>')
def get_user(user_id):
    user = get_user_by_id(user_id)
    if user is None:
        raise HTTPError(404, 'User not found')
    return json.dumps(user)

# Route to create a new user
@app.post('/users')
def create_user():
    try:
        user_data = request.json
        new_user = {"id": len(users) + 1, "name": user_data['name'], "email": user_data['email']}
        users.append(new_user)
        response.status = 201
        return json.dumps(new_user)
    except KeyError:
        raise HTTPError(400, 'Missing user details')
    except Exception as e:
        raise HTTPError(500, str(e))

# Route to update an existing user
@app.put('/users/<user_id:int>')
def update_user(user_id):
    user = get_user_by_id(user_id)
    if user is None:
        raise HTTPError(404, 'User not found')
    try:
        user_data = request.json
        user['name'] = user_data.get('name', user['name'])
        user['email'] = user_data.get('email', user['email'])
        return json.dumps(user)
    except KeyError:
        raise HTTPError(400, 'Missing user details')
    except Exception as e:
        raise HTTPError(500, str(e))

# Route to delete a user
@app.delete('/users/<user_id:int>')
def delete_user(user_id):
    global users
    user = get_user_by_id(user_id)
    if user is None:
        raise HTTPError(404, 'User not found')
    users = [u for u in users if u['id'] != user_id]
    return json.dumps({'message': 'User deleted'})

# Run the Bottle application
if __name__ == '__main__':
    run(app, host='localhost', port=8080)