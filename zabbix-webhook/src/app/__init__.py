# import asyncio
from flask import Flask, request, Response
from pyzabbix import ZabbixMetric, ZabbixSender
import requests
import time
import json
import os

# parameters
default_zabbix_server = '127.0.0.1'
default_zabbix_host = 'Zabbix-server'
default_zabbix_item = 'webhook'
azure_zabbix_item = 'az-mon'
awssns_zabbix_item = 'aws-sns'


app = Flask(__name__)

status = {'messages': [], 'status': 1,
            'started': int(time.time()),
            'timestamp': int(time.time()),
            'worker': os.getpid(),
            'counters': {
                'error': 0,
                'aws-sns': 0,
                'generic': 0,
                'az-mon': 0
            }
        }

  
def send_data_to_zabbix_server(server, hostname, key, js_data):
    # print('js_data:{}'.format(js_data))
    result = ZabbixSender(server).send(
        [ZabbixMetric(hostname, key, json.dumps(js_data), int(time.time()))]
    )
    print('send:result:{}'.format(result))
    return result


@app.route('/zabbix/aws-sns/', methods=['POST', 'PUT'])
def aws_sns_message():
    """
    Process AWS SNS messages : Subscription and Notification
        Collect POST payload from webhook and send it to Zabbix trapper item
    :return: HTTP/200+OK or HTTP/400
    """
    # AWS sends JSON with text/plain mimetype
    try:
        print('aws-sns:request:{}'.format(request.data))
        js_data = json.loads(request.data)
    except Exception as e:
        print('aws-sns:error loading payload:{}'.format(e), file=sys.stderr)
        status['counters']['error'] = status['counters']['error'] + 1
        return 'bad request!', 400

    hdr = request.headers.get('X-Amz-Sns-Message-Type')

    # subscribe to the SNS topic
    if hdr == 'SubscriptionConfirmation' and 'SubscribeURL' in js_data:
        result = requests.get(js_data['SubscribeURL'])
        print('aws-sns:SubscriptionConfirmation:result:{}'.format(result))
        if result.status_code != 200:
            return Response('aws-sns:Request to SubscribeURL failed. Unable to confirm subscription.', status=500)
        return Response('aws-sns:Subscription is successfully confirmed.', status=200)

    # forward notification payload to Zabbix trapper item
    if hdr == 'Notification':
        try:
            key = request.args.get('k', awssns_zabbix_item)
            server = request.args.get('s', default_zabbix_server)
            hostname = request.args.get('h', default_zabbix_host)

            # remove unwanted data as Zabbix item size is quite small
            if 'UnsubscribeURL' in js_data:
                del js_data['UnsubscribeURL']
            if 'SigningCertURL' in js_data:
                del js_data['SigningCertURL']
            if 'Signature' in js_data:
                del js_data['Signature']
            if 'SignatureVersion' in js_data:
                del js_data['SignatureVersion']

            send_data_to_zabbix_server(server, hostname, key, js_data)
            status['counters']['aws-sns'] = status['counters']['aws-sns'] + 1
        except Exception as e:
            print('aws-sns:error:{}'.format(e), file=sys.stderr)
            status['counters']['error'] = status['counters']['error'] + 1
            return 'bad request!', 400

    return 'OK\n'


@app.route('/zabbix/az-mon/', methods=['POST', 'PUT'])
def zbx_azure_monitor_webhook():
    """
    Process Azure Monitor messages
        Collect POST payload from webhook and send it to Zabbix trapper item
    :return: HTTP/200+OK or HTTP/400
    """
    try:
        print('az-mon:request:{}'.format(request.data))
        js_data = json.loads(request.data)
    except Exception as e:
        print('az-mon:error:{}'.format(e), file=sys.stderr)
        status['counters']['error'] = status['counters']['error'] + 1
        return 'bad request!', 400

    try:
        key = request.args.get('k', azure_zabbix_item)
        server = request.args.get('s', default_zabbix_server)
        hostname = request.args.get('h', default_zabbix_host)

        send_data_to_zabbix_server(server, hostname, key, js_data)
        status['counters']['az-mon'] = status['counters']['az-mon'] + 1
    except Exception as e:
        print('az-mon:error:{}'.format(e), file=sys.stderr)
        status['counters']['error'] = status['counters']['error'] + 1
        return 'bad request!', 400

    return 'OK\n'



@app.route('/zabbix/generic/', methods=['POST', 'PUT'])
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
        key = request.args.get('k', default_zabbix_item)
        server = request.args.get('s', default_zabbix_server)
        hostname = request.args.get('h', default_zabbix_host)

        send_data_to_zabbix_server(server, hostname, key, js_data)
        status['counters']['generic'] = status['counters']['generic'] + 1
    except Exception as e:
        print('generic:error:{}'.format(e), file=sys.stderr)
        status['counters']['error'] = status['counters']['error'] + 1
        return 'bad request!', 400

    return 'OK\n'


@app.route('/health', methods=['GET'])
def query_health():
    status['timestamp'] = int(time.time())
    return '{}'.format(json.dumps(status)), 200

@app.route('/help', methods=['GET'])
def query_help():
    help = { 'help': {
        'services': {
            'health': '[GET]/health',
            'aws-sns': '[POST,PUT]/zabbix/aws-sns/?k=[zabbix_item_key:-{}]&s=[zabbix_server_destination:-{}]&h=[zabbix_host_destination:-{}]'.format(default_zabbix_item, default_zabbix_server, default_zabbix_host),
            'az-mon': '[POST,PUT]/zabbix/az-mon/?k=[zabbix_item_key:-{}]&s=[zabbix_server_destination:-{}]&h=[zabbix_host_destination:-{}]'.format(default_zabbix_item, default_zabbix_server, default_zabbix_host),
            'generic': '[POST,PUT]/zabbix/generic/?k=[zabbix_item_key:-{}]&s=[zabbix_server_destination:-{}]&h=[zabbix_host_destination:-{}]'.format(default_zabbix_item, default_zabbix_server, default_zabbix_host),
        }
      }
    }
    return '{}'.format(json.dumps(help)), 200
