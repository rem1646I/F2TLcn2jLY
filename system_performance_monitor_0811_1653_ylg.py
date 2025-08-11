# 代码生成时间: 2025-08-11 16:53:59
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
System Performance Monitor using Bottle framework.
"""

from bottle import Bottle, run, template, static_file
import psutil
import os
import json

# Initialize the Bottle application
app = Bottle()

# Define a route to display the HTML page for system performance monitor
@app.route('/')
def index():
    return static_file('index.html', root='views')

# Define a route to get system information
@app.route('/info')
def get_system_info():
    try:
        # Gather system information
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_usage = psutil.virtual_memory().percent
        disk_usage = psutil.disk_usage('/').percent
        network_io = psutil.net_io_counters()
        system_info = {
            'cpu_usage': cpu_usage,
            'memory_usage': memory_usage,
            'disk_usage': disk_usage,
            'network_io': {
                'bytes_sent': network_io.bytes_sent,
                'bytes_recv': network_io.bytes_recv
            }
        }
        # Return system information as JSON
        return json.dumps(system_info)
    except Exception as e:
        return json.dumps({'error': str(e)})

# Define a route to serve static files like CSS, JS, and images
@app.route('/static/<filename:path>')
def server_static(filename):
    return static_file(filename, root='static')

# Run the application if this file is executed directly
if __name__ == '__main__':
    run(app, host='localhost', port=8080)
