"""
Goal: Manage Generic workloads
@authors:
    Gaël MONDON
"""
import sys

from fastapi import Depends, BackgroundTasks, Request, APIRouter, HTTPException

from app.config import status, defaults
from app.zabbix import send_data_to_zabbix_server
from app.tools import validate_json
from app.security import get_current_username

generic_route = APIRouter()


@generic_route.post("/zabbix/generic")
async def zbx_generic_webhook(background_tasks: BackgroundTasks,
                              request_data: Request,
                              auth: str = Depends(get_current_username),
                              k: str | None = defaults['generic_item_key'],
                              s: str | None = defaults['zabbix_server'],
                              h: str | None = defaults['zabbix_host']
                              ):
    """
    Process AWS SNS messages : Subscription and Notification
        Collect POST payload from webhook and send it to Zabbix trapper item
    :return: HTTP/200+OK or HTTP/400
    """
    status['counters']['generic']['received'] = status['counters']['generic']['received'] + 1
    try:
        json_data = await request_data.json()
        #print('generic:data:{}'.format(json_data))
    except Exception as e:
        print('generic:get json:error:{}'.format(e), file=sys.stderr)
        status['counters']['error'] = status['counters']['error'] + 1
        raise HTTPException(status_code=400, detail="bad request")

    if validate_json(json_data):
        try:
            background_tasks.add_task(send_data_to_zabbix_server, s, h, k, json_data)
            #print('generic:send_data_to_zabbix_server:server: {}, hostname: {}, key: {}'.format(s, h, k))
        except Exception as e:
            print('generic:send_data_to_zabbix_server:error:{}, server: {}, hostname: {}, key: {}'.format(e, s, h, k), file=sys.stderr)
            status['counters']['error'] = status['counters']['error'] + 1
            status['counters']['generic']['error'] = status['counters']['generic']['error'] + 1
            raise HTTPException(status_code=400, detail="bad request")

        return True
    else:
        raise HTTPException(status_code=400, detail="bad request")
