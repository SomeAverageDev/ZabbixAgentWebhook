"""
    Define global variables
"""
import time
import os

# parameters
defaults = {
    'username': 'user',
    'password': 'password',
    'zabbix_server': '127.0.0.1',
    'zabbix_host': 'Zabbix-server',
    'generic_item': 'webhook',
    'azure_item': 'az-mon',
    'awssns_item': 'aws-sns',
    'gcp_item': 'gcp',
}

status = {
    'messages': [],
    'status': 1,
    'started': int(time.time()),
    'timestamp': int(time.time()),
    'worker': os.getpid(),
    'counters': {
        'error': 0,
        'generic': 0,
        'aws-sns': 0,
        'az-mon': 0,
        'gcp': 0,
    }
}

fast_api_config = {
    'title': 'Zabbix Agent Webhook Listener',
    'version': '0.0.1',
    'docs_url': '/help',
    'redoc_url': None,
    'description': """
Provides API Listeners for CSP alerts and events

You will be able to collect JSON payloads from CSP services below:

* **Google Cloud Platform Alerts**
* **Amazon Web Services SNS**
* **Azure Monitor Alerts**

It also provides a generic interface
"""
}
