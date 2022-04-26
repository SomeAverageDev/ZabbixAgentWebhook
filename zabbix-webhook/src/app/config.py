""""
Goal: Define global variables
@authors:
    Gaël MONDON
"""
import time
import os

# parameters
defaults = {
    'username': 'user',
    'password': 'password',
    'zabbix_server': '127.0.0.1',
    'zabbix_host': 'Zabbix server',
    'generic_item_key': 'zwl.webhook',
    'azure_item_key': 'zwl.az-mon',
    'awssns_item_key': 'zwl.aws-sns',
    'gcp_item_key': 'zwl.gcp',
    'awssns_subscribe-url-validation': '.amazonaws.com/?Action=ConfirmSubscription',
}

"""
 Setting defaults from environment variables
"""
for key in defaults:
    defaults[key] = os.getenv('ZWL_' + key.upper(), defaults[key])

# FastAPI config
fast_api_config = {
    'title': 'Zabbix Agent Webhook Listener',
    'version': '0.0.1',
    'docs_url': '/help',
    'redoc_url': None,
    'description': """
## *Provides API Listeners for generic and main Cloud Services Providers alerts and events*

You will be able to collect JSON payloads from CSP services below:

* **Google Cloud Platform Alerts**
* **Amazon Web Services SNS**
* **Azure Monitor Alerts**
* It also provides a **generic** interface

### Cloud Providers configurations
Configure CSP Webhooks to the related Zabbix Agent Webhook Listener API endpoint below

### API CALLS ARGUMENTS
* **s** : Overrides default ZWL_ZABBIX_SERVER parameter
* **h** : Overrides default ZWL_ZABBIX_HOST parameter
* **k** : Overrides default Zabbix item key parameter

### DOCKER IMAGE
* Docker image will listen on default port **80**
* Docker image uses **gunicorn** as process manager
* Docker image uses **uvicorn** as ASGI web server
* Docker image will start with 1 worker and 4 threads 
* You can override default **CMD** command

#### DOCKER IMAGE ENVIRONMENT VARIABLES
* **ZWL_BIND** : Application binding IP address, default : '0.0.0.0'
* **ZWL_PORT** : Application binding port, default : '80'
* **ZWL_WORKERS** : Gunicorn workers number, default : '1'
* **ZWL_THREADS** : Gunicorn threads number, default : '4'

### APPLICATION ENVIRONMENT VARIABLES
* **ZWL_USERNAME** : Username for authentication, default : 'user'
* **ZWL_PASSWORD** : Password for authentication, default : 'password'
* **ZWL_ZABBIX_SERVER** : Zabbix Server destination **IP address** or FQDN, default : '127.0.0.1'
* **ZWL_ZABBIX_HOST** : Name of the host collecting data, **it must be linked to Zabbix template**, default : 'Zabbix server'
* **ZWL_GENERIC_ITEM_KEY** : Name of the Zabbix item to collect generic payload, default : 'zwl.webhook'
* **ZWL_AZURE_ITEM_KEY** : Name of the Zabbix item to collect Azure payload, default : 'zwl.az-mon'
* **ZWL_AWSSNS_ITEM_KEY** : Name of the Zabbix item to collect AWS SNS Events payload, default : 'zwl.aws-sns'
* **ZWL_GCP_ITEM_KEY** : Name of the Zabbix item to collect Google Cloud Platform Monitoring alerts payload, default : 'zwl.gcp'

"""
}

# application stats
status = {
    'messages': [],
    'status': 1,
    'started': int(time.time()),
    'timestamp': int(time.time()),
    'worker': os.getpid(),
    'counters': {
        'error': 0,
        'generic': {'received': 0, 'error': 0},
        'aws-sns': {'received': 0, 'error': 0},
        'az-mon': {'received': 0, 'error': 0},
        'gcp': {'received': 0, 'error': 0},
    }
}
