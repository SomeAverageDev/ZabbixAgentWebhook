"""
Goal: Manager Zabbix data
@authors:
    Gaël MONDON
"""
import time
import json

from pyzabbix import ZabbixMetric, ZabbixSender


def send_data_to_zabbix_server(server, hostname, key, json_data):
    # print('js_data:{}'.format(json_data))
    result = ZabbixSender(server).send(
        [ZabbixMetric(hostname, key, json.dumps(json_data), int(time.time()))]
    )
    print('send:result:{}'.format(result))
    return result
