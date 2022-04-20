# Zabbix Agent Webhook Listener
** THIS IS STILL UNDER HEAVY DEVELOPMENT **

# *Provides API Listeners for generic and main Cloud Services Providers alerts and events*

## Description
Zabbix Agent Webhook Listener can handle various JSON data sent from tier services.
This project build a Docker image that hosts a Python's webhook listener to forward and process JSON data to Zabbix item

## Installation
### Docker Image
Deploy the Docker Image

### Zabbix template
Import the [template file] into Zabbix server (_template/CMS_ZBX_WEBHOOK_TPL.xml)


### Cloud Providers configurations
Configure CSP Webhooks to the related Zabbix Agent Webhook Listener API endpoint


## Usage & Parameters
You will be able to collect JSON payloads from CSP services below:

* **Google Cloud Platform Alerts**
* **Amazon Web Services SNS**
* **Azure Monitor Alerts**
* It also provides a **generic** interface

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
* **ZWL_USERNAME** : Username for Zabbix Agent Webhook Listener authentication, default : 'user'
* **ZWL_PASSWORD** : Password for Zabbix Agent Webhook Listener authentication, default : 'password'
* **ZWL_ZABBIX_SERVER** : Zabbix Server destination **IP address** or FQDN, default : '127.0.0.1'
* **ZWL_ZABBIX_HOST** : Name of the host collecting data, **it must be linked to Zabbix template**, default : 'Zabbix server'
* **ZWL_GENERIC_ITEM** : Name of the Zabbix item to collect generic payload, default : 'webhook'
* **ZWL_AZURE_ITEM** : Name of the Zabbix item to collect Azure payload, default : 'az-mon'
* **ZWL_AWSSNS_ITEM** : Name of the Zabbix item to collect AWS SNS Events payload, default : 'aws-sns'
* **ZWL_GCP_ITEM** : Name of the Zabbix item to collect Google Cloud Platform Monitoring alerts payload, default : 'gcp'
