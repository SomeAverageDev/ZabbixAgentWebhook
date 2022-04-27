"""
Goal: Manage Azure workloads
@authors:
    Gaël MONDON
documentation:https://docs.microsoft.com/fr-fr/azure/azure-monitor/alerts/alerts-common-schema-definitions
"""
import sys

from fastapi import Depends, BackgroundTasks, Request, APIRouter, HTTPException

from app.config import status, defaults
from app.zabbix import send_data_to_zabbix_server
from app.tools import validate_json
from app.security import get_current_username


azure_route = APIRouter()


@azure_route.post('/zabbix/azure/common')
async def zbx_azure_monitor_webhook(background_tasks: BackgroundTasks,
                                    request_data: Request,
                                    auth: str = Depends(get_current_username),
                                    k: str | None = defaults['azure_item_key'],
                                    s: str | None = defaults['zabbix_server'],
                                    h: str | None = defaults['zabbix_host']
                                    ):
    """
    Process Azure Monitor common messages
        Collect POST payload from webhook and send it to Zabbix trapper item
    :return: HTTP/200+OK or HTTP/400
    """
    status['counters']['az-mon']['received'] = status['counters']['az-mon']['received'] + 1
    try:
        json_data = await request_data.json()
        #print('az-mon:data:{}'.format(json_data))
    except Exception as e:
        print('az-mon:error:{}'.format(e), file=sys.stderr)
        status['counters']['error'] = status['counters']['error'] + 1
        raise HTTPException(status_code=406)

    if validate_json(json_data):
        try:
            background_tasks.add_task(send_data_to_zabbix_server, s, h, k, json_data)
            #print('az-mon:send_data_to_zabbix_server:server: {}, hostname: {}, key: {}; data:{}'.format(s, h, k, json_data))
        except Exception as e:
            print('az-mon:error:{}'.format(e), file=sys.stderr)
            status['counters']['error'] = status['counters']['error'] + 1
            status['counters']['az-mon']['error'] = status['counters']['az-mon']['error'] + 1
            raise HTTPException(status_code=406)

        return True
    else:
        raise HTTPException(status_code=400)
