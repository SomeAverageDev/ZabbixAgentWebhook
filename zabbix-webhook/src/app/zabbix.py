"""
Goal: Manager Zabbix data exchange
@authors:
    Gaël MONDON
"""
import sys
import time
import json

from pyzabbix import ZabbixMetric, ZabbixSender
from app.config import status, defaults


def send_data_to_zabbix_server(server, hostname, key, json_data, port=10051):
    # print('js_data:{}'.format(json_data))
    if defaults['allow_override_server'] is False:
        server = defaults['zabbix_server']
    
    try:
        result = ZabbixSender(zabbix_server=server, zabbix_port=port).send(
            [ZabbixMetric(hostname, key, json.dumps(json_data), int(time.time()))]
        )
#        print('send_data_to_zabbix_server:{}/{}/{}:result:{}'.format(server, hostname, key, result))

        if result.failed != 0:
            status['counters']['error'] = status['counters']['error'] + 1
            print('send_data_to_zabbix_server:{}/{}/{}:error:{}'.format(server, hostname, key, result))

    except Exception as e:
        print('send_data_to_zabbix_server:{}/{}/{}:exception:{}'.format(server, hostname, key, e), file=sys.stderr)
        return None

    return True
