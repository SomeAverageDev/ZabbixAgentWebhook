"""
Goal: Manage Azure workloads
@authors:
    Gaël MONDON
documentation:https://docs.microsoft.com/fr-fr/azure/azure-monitor/alerts/alerts-common-schema-definitions
"""
import sys
import json

from flask import request, Blueprint
from app.config import status, defaults
from app.zabbix import send_data_to_zabbix_server


azure_route = Blueprint('azure_route', __name__)


@azure_route.route('/zabbix/az-mon/', methods=['POST', 'PUT'])
def zbx_azure_monitor_webhook():
    """
    Process Azure Monitor messages
        Collect POST payload from webhook and send it to Zabbix trapper item
    :return: HTTP/200+OK or HTTP/400
    """
    try:
        print('az-mon:request:{}'.format(request.data))
        js_data = json.loads(request.data)
    except Exception as e:
        print('az-mon:error:{}'.format(e), file=sys.stderr)
        status['counters']['error'] = status['counters']['error'] + 1
        return 'bad request!', 400

    try:
        key = request.args.get('k', defaults['azure_item'])
        server = request.args.get('s', defaults['zabbix_server'])
        hostname = request.args.get('h', defaults['zabbix_host'])

        send_data_to_zabbix_server(server, hostname, key, js_data)
        status['counters']['az-mon'] = status['counters']['az-mon'] + 1
    except Exception as e:
        print('az-mon:error:{}'.format(e), file=sys.stderr)
        status['counters']['error'] = status['counters']['error'] + 1
        return 'bad request!', 400

    return 'OK\n'
