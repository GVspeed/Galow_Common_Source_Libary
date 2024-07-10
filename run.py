import subprocess
import os
import time

# Verzeichnisse, in denen sich die Skripte befinden
adminportal_dir = os.path.join(os.path.dirname(__file__), 'adminportal')
admindashboard_dir = os.path.join(os.path.dirname(__file__), 'admindashboard')

# Pfade zu den Skripten
adminportal_path = os.path.join(adminportal_dir, 'adminportal.py')
admindashboard_path = os.path.join(admindashboard_dir, 'admindashboard.py')

# Start adminportal.py
adminportal_process = subprocess.Popen(['python', adminportal_path], shell=True)
print("Started adminportal.py with PID:", adminportal_process.pid)

# Give it some time to start before starting the dashboard
time.sleep(5)

# Start admindashboard.py
admindashboard_process = subprocess.Popen(['python', admindashboard_path], shell=True)
print("Started admindashboard.py with PID:", admindashboard_process.pid)

# Wait for both processes to complete
try:
    adminportal_process.wait()
    admindashboard_process.wait()
except KeyboardInterrupt:
    print("Stopping both processes...")
    adminportal_process.terminate()
    admindashboard_process.terminate()