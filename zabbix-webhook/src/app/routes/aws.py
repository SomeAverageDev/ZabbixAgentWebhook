"""
Goal: Manage AWS workloads
@authors:
    Gaël MONDON
"""
import sys
import requests

from fastapi import Depends, BackgroundTasks, Request, APIRouter, HTTPException, Header
from app.config import status, defaults
from app.zabbix import send_data_to_zabbix_server
from app.tools import validate_json
from app.security import get_current_username


aws_route = APIRouter()


@aws_route.post('/zabbix/aws-sns/')
async def aws_sns_message(background_tasks: BackgroundTasks,
                          request_data: Request,
                          auth: str = Depends(get_current_username),
                          x_amz_sns_message_type: str | None = Header(None),
                          k: str | None = defaults['awssns_item'],
                          s: str | None = defaults['zabbix_server'],
                          h: str | None = defaults['zabbix_host']
                          ):
    """
    Process AWS SNS messages : Subscription and Notification
        Collect POST payload from webhook and send it to Zabbix trapper item
    :return: HTTP/200+OK or HTTP/400
    """
    # AWS sends JSON with text/plain mimetype
    try:
        json_data = await request_data.json()
        #print('aws-sns:data:{}'.format(json_data))
    except Exception as e:
        print('aws-sns:error loading payload:{}'.format(e), file=sys.stderr)
        status['counters']['error'] = status['counters']['error'] + 1
        raise HTTPException(status_code=400, detail="bad request")

    if x_amz_sns_message_type == 'SubscriptionConfirmation' and 'SubscribeURL' in json_data:
        # subscribe to the SNS topic
        print('SubscribeURL:{}'.format(json_data['SubscribeURL']))
        result = requests.get(json_data['SubscribeURL'])
        print('aws-sns:SubscriptionConfirmation:result:{}'.format(result))
        if result.status_code != 200:
            raise HTTPException(status_code=result.status_code, detail="bad request")
        return True

    if x_amz_sns_message_type is not None and x_amz_sns_message_type == 'Notification':
        if validate_json(json_data):
            # forward notification payload to Zabbix trapper item
            try:
                # remove unwanted data as Zabbix item size is quite small
                if 'UnsubscribeURL' in json_data:
                    del json_data['UnsubscribeURL']
                if 'SigningCertURL' in json_data:
                    del json_data['SigningCertURL']
                if 'Signature' in json_data:
                    del json_data['Signature']
                if 'SignatureVersion' in json_data:
                    del json_data['SignatureVersion']

                background_tasks.add_task(send_data_to_zabbix_server, s, h, k, json_data)
                #print('aws-sns:send_data_to_zabbix_server:server: {}, hostname: {}, key: {}; data:{}'.format(s, h, k, json_data))
                status['counters']['aws-sns'] = status['counters']['aws-sns'] + 1
            except Exception as e:
                print('aws-sns:error:{}'.format(e), file=sys.stderr)
                status['counters']['error'] = status['counters']['error'] + 1
                raise HTTPException(status_code=400, detail="bad request")

            return True

    raise HTTPException(status_code=400, detail="bad request")
