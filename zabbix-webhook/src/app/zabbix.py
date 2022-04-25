"""
Goal: Manager Zabbix data
@authors:
    Gaël MONDON
"""
import sys
import time
import json

from pyzabbix import ZabbixMetric, ZabbixSender
from app.config import status


def send_data_to_zabbix_server(server, hostname, key, json_data):
    # print('js_data:{}'.format(json_data))
    try:
        result = ZabbixSender(server).send(
            [ZabbixMetric(hostname, key, json.dumps(json_data), int(time.time()))]
        )
#        print('send_data_to_zabbix_server:result:{}'.format(result))

        if result.failed != 0:
            status['counters']['error'] = status['counters']['error'] + 1
            print('send_data_to_zabbix_server:error:{}'.format(result))

    except Exception as e:
        print('send_data_to_zabbix_server:exception:{}'.format(e), file=sys.stderr)
        return None

    return True
