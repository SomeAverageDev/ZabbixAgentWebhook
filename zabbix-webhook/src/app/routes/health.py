"""
Goal: Manage health
@authors:
    Gaël MONDON
"""
import time
import json

from flask import Blueprint
try:
    from app.config import status
except:
    from .app.config import status

health_route = Blueprint('health_route', __name__)


@health_route.route('/health', methods=['GET'])
def query_health():
    status['timestamp'] = int(time.time())
    return '{}'.format(json.dumps(status)), 200

