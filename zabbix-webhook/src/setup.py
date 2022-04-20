from setuptools import setup, find_packages


LONG_DESCRIPTION = 'Zabbix Agent Webhook Listener can handle various JSON data sent from tier services.'

DEPENDENCIES = [
    'py-zabbix==1.1.7',
    'gunicorn==20.1.0',
    'uvicorn==0.17.6',
    'requests>=2.24.0',
    'fastapi==0.75.2',
]

EXCLUDED_PACKAGES = [
]

setup(
    name='zabbix-agent-webhook',
    version='0.0.1',
    description='Zabbix Agent Webhook Listener',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text',
    author='https://github.com/SomeAverageDev/ZabbixMaintenance',
    url='https://github.com/SomeAverageDev/ZabbixAgentWebhook/',
    python_requires='>=3.9',
    install_requires=DEPENDENCIES,
    packages=find_packages(exclude=EXCLUDED_PACKAGES),
)