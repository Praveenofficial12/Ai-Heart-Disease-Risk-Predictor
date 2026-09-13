import sys
import os
import traceback

# Add backend directory and project root to Python path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, ".."))
BACKEND_DIR = os.path.join(PROJECT_ROOT, "backend")

if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

try:
    from app import app
    handler = app
except Exception as err:
    error_trace = traceback.format_exc()
    print("Vercel App Initialization Exception:\n", error_trace)
    from flask import Flask
    app = Flask(__name__)
    @app.route("/")
    @app.route("/<path:path>")
    def error_page(path=""):
        return f"<h2>Application Startup Error</h2><pre>{error_trace}</pre>", 500
    handler = app
