# 代码生成时间: 2025-08-21 04:54:44
#!/usr/bin/env python

"""
Scheduled Task Scheduler using the Bottle framework.
This script creates a simple web server that runs a scheduled task periodically.
"""

import bottle
import time
from threading import Thread
from datetime import datetime

# Constants for scheduled task settings
INTERVAL = 10  # Interval in seconds
TASK_RUNNING = False

# This function will be the scheduled task to be run periodically
def scheduled_task():
    """
    This function is an example of a scheduled task.
    It writes the current time to a log file named 'scheduled_task_log.txt'.
    """
    with open('scheduled_task_log.txt', 'a') as log_file:
        log_file.write(datetime.now().isoformat() + '
')
    print("Scheduled task executed at:", datetime.now())

# This function sets up the periodic execution of the scheduled_task function
def run_periodic_task():
    global TASK_RUNNING
    while TASK_RUNNING:
        scheduled_task()
        time.sleep(INTERVAL)

# Initialize Bottle app
app = bottle.Bottle()

# Web route to start the scheduled task
@app.route('/start_task')
def start_task():
    global TASK_RUNNING
    if not TASK_RUNNING:
        TASK_RUNNING = True
        task_thread = Thread(target=run_periodic_task)
        task_thread.start()
        return {'status': 'Task started'}
    else:
        return {'status': 'Task already running'}

# Web route to stop the scheduled task
@app.route('/stop_task')
def stop_task():
    global TASK_RUNNING
    if TASK_RUNNING:
        TASK_RUNNING = False
        return {'status': 'Task stopped'}
    else:
        return {'status': 'Task is not running'}

# Run the Bottle app if this script is executed directly
if __name__ == '__main__':
    # Start the Bottle server on port 8080
    app.run(host='localhost', port=8080, debug=True)
