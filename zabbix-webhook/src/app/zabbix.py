"""
Goal: Manager Zabbix data
@authors:
    Gaël MONDON
"""
import json
import time

from pyzabbix import ZabbixMetric, ZabbixSender


def send_data_to_zabbix_server(server, hostname, key, js_data):
    # print('js_data:{}'.format(js_data))
    result = ZabbixSender(server).send(
        [ZabbixMetric(hostname, key, json.dumps(js_data), int(time.time()))]
    )
    print('send:result:{}'.format(result))
    return result
