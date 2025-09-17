# 代码生成时间: 2025-09-18 03:28:19
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A simple configuration manager using Bottle framework.
This script provides a web service with endpoints to retrieve and update configuration files.
"""

import bottle
import json
import os
from bottle import redirect

# Define the directory where configuration files are stored.
CONFIG_DIR = 'configs/'

# Ensure the configuration directory exists.
if not os.path.exists(CONFIG_DIR):
    os.makedirs(CONFIG_DIR)

# Define the API endpoints.
@bottle.route('/config/<config_name:path>', method='GET')
def get_config(config_name):
    """Retrieve a configuration file."""
    file_path = os.path.join(CONFIG_DIR, config_name)
    if not os.path.isfile(file_path):
        return bottle.HTTPResponse(status=404, body=json.dumps({'error': 'Config file not found'}), content_type='application/json')
    with open(file_path, 'r') as file:
        config_data = file.read()
    return json.dumps({'config': config_data})

@bottle.route('/config/<config_name:path>', method='PUT')
def update_config(config_name):
    """Update a configuration file."""
    file_path = os.path.join(CONFIG_DIR, config_name)
    if not bottle.request.json:
        return bottle.HTTPResponse(status=400, body=json.dumps({'error': 'No JSON data provided'}), content_type='application/json')
    config_data = bottle.request.json
    try:
        with open(file_path, 'w') as file:
            file.write(json.dumps(config_data))
    except IOError as e:
        return bottle.HTTPResponse(status=500, body=json.dumps({'error': 'Failed to write to config file'}), content_type='application/json')
    return json.dumps({'message': 'Config updated successfully'})

@bottle.route('/config/<config_name:path>', method='DELETE')
def delete_config(config_name):
    """Delete a configuration file."""
    file_path = os.path.join(CONFIG_DIR, config_name)
    try:
        os.remove(file_path)
    except OSError as e:
        return bottle.HTTPResponse(status=500, body=json.dumps({'error': 'Failed to delete config file'}), content_type='application/json')
    return json.dumps({'message': 'Config deleted successfully'})

@bottle.error(404)
def error_404(error):
    """Custom 404 error handler."""
    return json.dumps({'error': 'Resource not found'})

if __name__ == '__main__':
    bottle.run(host='localhost', port=8080, debug=True)
