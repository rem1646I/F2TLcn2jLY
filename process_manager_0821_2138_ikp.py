# 代码生成时间: 2025-08-21 21:38:56
#!/usr/bin/env python
"""
Process Manager using Bottle framework.
This script allows you to manage processes, including starting, stopping, and listing them.
"""

import bottle
import subprocess
import os
import signal
import psutil
from threading import Thread


# Constants for listing processes
LIST_PROCESSES = '/proc/'

# Route for listing all running processes
@bottle.route('/processes', method='GET')
def list_processes():
    """
    List all running processes.
    """
    processes = []
    for proc in psutil.process_iter(['pid', 'name']):
        processes.append({'pid': proc.info['pid'], 'name': proc.info['name']})
    return bottle.response.json({'processes': processes})

# Route for starting a new process
@bottle.route('/start/<process_name:path>', method='POST')
def start_process(process_name):
    """
    Start a new process with the given name.
    Returns the PID of the new process or an error message.
    """
    try:
        process = subprocess.Popen([process_name])
        return bottle.response.json({'pid': process.pid, 'message': 'Process started successfully.'})
    except Exception as e:
        return bottle.response.json({'error': str(e)})

# Route for stopping a process by name
@bottle.route('/stop/<process_name:path>', method='POST')
def stop_process(process_name):
    """
    Stop a process by its name.
    Returns a success message or an error message.
    """
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == process_name:
            try:
                proc.send_signal(signal.SIGTERM)
                return bottle.response.json({'message': 'Process stopped successfully.'})
            except Exception as e:
                return bottle.response.json({'error': str(e)})
    return bottle.response.json({'error': 'Process not found.'})

# Route for stopping a process by PID
@bottle.route('/stop/<pid:int>', method='POST')
def stop_process_by_pid(pid):
    """
    Stop a process by its PID.
    Returns a success message or an error message.
    """
    try:
        process = psutil.Process(pid)
        process.send_signal(signal.SIGTERM)
        return bottle.response.json({'message': 'Process stopped successfully.'})
    except psutil.NoSuchProcess:
        return bottle.response.json({'error': 'Process not found.'})
    except Exception as e:
        return bottle.response.json({'error': str(e)})

# Start the Bottle server
if __name__ == '__main__':
    bottle.run(host='localhost', port=8080, debug=True)