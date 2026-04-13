import subprocess
import sys
import os
import webbrowser
import threading

# Paths
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
BACKEND_PATH = os.path.join(PROJECT_ROOT, "backend")
FRONTEND_PATH = os.path.join(PROJECT_ROOT, "frontend")

# Function to run backend
def run_backend():
    os.chdir(BACKEND_PATH)
    # Run Flask app
    subprocess.run([sys.executable, "app.py"])

# Function to run frontend server
def run_frontend():
    os.chdir(FRONTEND_PATH)
    # Serve frontend on port 8000
    subprocess.run([sys.executable, "-m", "http.server", "8000"])

# Open browser after a short delay
def open_browser():
    import time
    time.sleep(3)  # wait for servers to start
    webbrowser.open("http://127.0.0.1:8000/index.html")

# Run backend and frontend in separate threads
threading.Thread(target=run_backend).start()
threading.Thread(target=run_frontend).start()
threading.Thread(target=open_browser).start()
