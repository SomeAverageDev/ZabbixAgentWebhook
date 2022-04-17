"""
Goal: Manage Google Cloud Platform workloads
@authors:
    Gaël MONDON
"""
import sys
import json

from flask import request, Blueprint
from app.config import status, defaults
from app.zabbix import send_data_to_zabbix_server


gcp_route = Blueprint('gcp_route', __name__)


@gcp_route.route('/zabbix/gcp/', methods=['POST', 'PUT'])
def zbx_google_cloud_webhook():
    """
    Process Google Cloud messages
        Collect POST payload from webhook and send it to Zabbix trapper item
    :return: HTTP/200+OK or HTTP/400
    """
    try:
        print('gcp:request:{}'.format(request.data))
        js_data = json.loads(request.data)
    except Exception as e:
        print('gcp:error:{}'.format(e), file=sys.stderr)
        status['counters']['error'] = status['counters']['error'] + 1
        return 'bad request!', 400

    try:
        key = request.args.get('k', defaults['gcp_item'])
        server = request.args.get('s', defaults['zabbix_server'])
        hostname = request.args.get('h', defaults['zabbix_host'])

        send_data_to_zabbix_server(server, hostname, key, js_data)
        status['counters']['gcp'] = status['counters']['gcp'] + 1
    except Exception as e:
        print('gcp:error:{}'.format(e), file=sys.stderr)
        status['counters']['error'] = status['counters']['error'] + 1
        return 'bad request!', 400

    return 'OK\n'
