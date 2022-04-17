"""
Goal: Manage Generic workloads
@authors:
    Gaël MONDON
"""
import sys
import json

from flask import request, Blueprint
from app.config import status, defaults
from app.zabbix import send_data_to_zabbix_server


generic_route = Blueprint('generic_route', __name__)


@generic_route.route('/zabbix/generic/', methods=['POST', 'PUT'])
def zbx_generic_webhook():
    """
    Process AWS SNS messages : Subscription and Notification
        Collect POST payload from webhook and send it to Zabbix trapper item
    :return: HTTP/200+OK or HTTP/400
    """
    try:
        print('generic:request:{}'.format(request.data))
        js_data = json.loads(request.data)
    except Exception as e:
        print('generic:error:{}'.format(e), file=sys.stderr)
        status['counters']['error'] = status['counters']['error'] + 1
        return 'bad request!', 400

    try:
        key = request.args.get('k', defaults['generic_item'])
        server = request.args.get('s', defaults['zabbix_server'])
        hostname = request.args.get('h', defaults['zabbix_host'])

        send_data_to_zabbix_server(server, hostname, key, js_data)
        status['counters']['generic'] = status['counters']['generic'] + 1
    except Exception as e:
        print('generic:error:{}'.format(e), file=sys.stderr)
        status['counters']['error'] = status['counters']['error'] + 1
        return 'bad request!', 400

    return 'OK\n'