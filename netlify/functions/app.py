import sys
import os
from serverless_wsgi import handle_request

# Add the project root to the python path so `app` can be imported
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
if project_root not in sys.path:
    sys.path.append(project_root)

from app import app as flask_app

def handler(event, context):
    return handle_request(flask_app, event, context)
