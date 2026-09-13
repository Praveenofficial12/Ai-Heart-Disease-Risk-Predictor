import sys
import os
import webbrowser
import threading
import time

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
BACKEND_PATH = os.path.join(PROJECT_ROOT, "backend")

if BACKEND_PATH not in sys.path:
    sys.path.insert(0, BACKEND_PATH)

def open_browser():
    time.sleep(1.5)
    webbrowser.open("http://127.0.0.1:5000/")

def run_server():
    from backend.app import app
    app.run(host="127.0.0.1", port=5000, debug=False)

if __name__ == "__main__":
    threading.Thread(target=open_browser, daemon=True).start()
    run_server()
