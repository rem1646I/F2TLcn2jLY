# 代码生成时间: 2025-09-02 20:26:24
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
System performance monitoring tool using Python and Bottle framework.
"""

import bottle
import os
import psutil
import json
from datetime import datetime

# Define your route and associated handler functions below

@bottle.route('/get_system_info')
def get_system_info():
    """
    Get system information.
    """
    try:
        # Get CPU usage
        cpu_usage = psutil.cpu_percent(interval=1)
        
        # Get memory usage
        mem = psutil.virtual_memory()
        memory_usage = mem.percent
        
        # Get disk usage
        disk_usage = psutil.disk_usage('/')
        total, used, free, percent = disk_usage
        
        # Get uptime
        uptime = psutil.uptime()
        
        # Format the response as JSON
        response = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'cpu_usage': cpu_usage,
            'memory_usage': memory_usage,
            'disk_usage': percent,
            'uptime': uptime
        }
        return bottle.response.json(response)
    except Exception as e:
        return bottle.response.json({'error': str(e)})

@bottle.route('/health_check')
def health_check():
    """
    Perform a simple health check by returning a success message.
    """
    try:
        # Perform any necessary checks to determine system health
        # For simplicity, just return a success message
        return bottle.response.json({'status': 'success'})
    except Exception as e:
        return bottle.response.json({'error': str(e)})


def run_server():
    """
    Run the Bottle server.
    """
    bottle.run(host='localhost', port=8080, debug=False)

if __name__ == '__main__':
    run_server()