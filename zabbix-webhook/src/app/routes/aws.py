"""
Goal: Manage AWS workloads
@authors:
    Gaël MONDON
"""
import sys
import json
import requests

from flask import request, Response, Blueprint
from app.config import status, defaults
from app.zabbix import send_data_to_zabbix_server


aws_route = Blueprint('aws_route', __name__)

@aws_route.route('/zabbix/aws-sns/', methods=['POST', 'PUT'])
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
            key = request.args.get('k', defaults['awssns_item'])
            server = request.args.get('s', defaults['zabbix_server'])
            hostname = request.args.get('h', defaults['zabbix_host'])

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