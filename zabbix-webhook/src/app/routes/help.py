"""
Goal: Manage help
@authors:
    Gaël MONDON
"""
import json

from flask import Blueprint
from app.config import defaults


help_route = Blueprint('help_route', __name__)


@help_route.route('/help', methods=['GET'])
def query_help():
    help_json = {'help': {
            'services': {
                'health': '[GET]/health',
                'gcp': '[POST,PUT]/zabbix/gcp/?k=[zabbix_item_key:-{}]&s=[zabbix_server_destination:-{}]&h=[zabbix_host_destination:-{}]'.format(
                    defaults['generic_item'], defaults['zabbix_server'], defaults['zabbix_host']),
                'aws-sns': '[POST,PUT]/zabbix/aws-sns/?k=[zabbix_item_key:-{}]&s=[zabbix_server_destination:-{}]&h=[zabbix_host_destination:-{}]'.format(
                    defaults['generic_item'], defaults['zabbix_server'], defaults['zabbix_host']),
                'az-mon': '[POST,PUT]/zabbix/az-mon/?k=[zabbix_item_key:-{}]&s=[zabbix_server_destination:-{}]&h=[zabbix_host_destination:-{}]'.format(
                    defaults['generic_item'], defaults['zabbix_server'], defaults['zabbix_host']),
                'generic': '[POST,PUT]/zabbix/generic/?k=[zabbix_item_key:-{}]&s=[zabbix_server_destination:-{}]&h=[zabbix_host_destination:-{}]'.format(
                    defaults['generic_item'], defaults['zabbix_server'], defaults['zabbix_host']),
            }
        }
    }
    return '{}'.format(json.dumps(help_json)), 200
