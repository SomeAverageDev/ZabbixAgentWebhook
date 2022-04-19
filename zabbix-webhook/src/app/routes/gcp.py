"""
Goal: Manage Google Cloud Platform workloads
@authors:
    Gaël MONDON
"""
import sys

from fastapi import Depends, BackgroundTasks, Request, APIRouter, HTTPException

from app.config import status, defaults
from app.zabbix import send_data_to_zabbix_server
from app.tools import validate_json
from app.security import get_current_username


gcp_route = APIRouter()


@gcp_route.post('/zabbix/gcp')
async def zbx_google_cloud_webhook(background_tasks: BackgroundTasks,
                                   request_data: Request,
                                   auth: str = Depends(get_current_username),
                                   k: str | None = defaults['gcp_item'],
                                   s: str | None = defaults['zabbix_server'],
                                   h: str | None = defaults['zabbix_host']
                                   ):
    """
    Process Google Cloud messages
        Collect POST payload from webhook and send it to Zabbix trapper item
    :return: HTTP/200+OK or HTTP/400
    """
    try:
        json_data = await request_data.json()
        #print('gcp:data:{}'.format(json_data))
    except Exception as e:
        print('gcp:error:{}'.format(e), file=sys.stderr)
        status['counters']['error'] = status['counters']['error'] + 1
        raise HTTPException(status_code=400, detail="bad request")

    if validate_json(json_data):
        try:
            background_tasks.add_task(send_data_to_zabbix_server, s, h, k, json_data)
            #print('gcp:send_data_to_zabbix_server:server: {}, hostname: {}, key: {}; data:{}'.format(s, h, k, json_data))
            status['counters']['gcp'] = status['counters']['gcp'] + 1
        except Exception as e:
            print('gcp:error:{}'.format(e), file=sys.stderr)
            status['counters']['error'] = status['counters']['error'] + 1
            raise HTTPException(status_code=400, detail="bad request")

        return True
    else:
        raise HTTPException(status_code=400, detail="bad request")
