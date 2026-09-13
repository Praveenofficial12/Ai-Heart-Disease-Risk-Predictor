import sys
import os

# Add backend directory and project root to Python system path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, ".."))
BACKEND_DIR = os.path.join(PROJECT_ROOT, "backend")

if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from backend.app import app as flask_app

class VercelWSGIMiddleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        matched_path = (
            environ.get('HTTP_X_MATCHED_PATH') or
            environ.get('x-matched-path') or
            environ.get('HTTP_X_REWRITE_URL')
        )
        if matched_path and not matched_path.startswith('/api'):
            environ['PATH_INFO'] = matched_path
        else:
            path = environ.get('PATH_INFO', '')
            if path.startswith('/api/index'):
                rest = path[10:]
                if rest and rest != '/':
                    environ['PATH_INFO'] = rest
                elif not matched_path:
                    environ['PATH_INFO'] = '/'

        proto = environ.get('HTTP_X_FORWARDED_PROTO', '')
        if proto.lower() == 'https':
            environ['wsgi.url_scheme'] = 'https'

        host = environ.get('HTTP_X_FORWARDED_HOST')
        if host:
            environ['HTTP_HOST'] = host

        return self.app(environ, start_response)

# Top-level application exports for Vercel Python Runtime
app = VercelWSGIMiddleware(flask_app)
handler = app
