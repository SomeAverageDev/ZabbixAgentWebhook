"""
Goal: Manage health response
@authors:
    Gaël MONDON
"""
import time

from fastapi import Depends, APIRouter
from fastapi.responses import JSONResponse

from app.config import status
from app.security import get_current_username


health_route = APIRouter()


@health_route.get('/health')
def query_status():
    return True


@health_route.get('/health/stats')
def query_health(auth: str = Depends(get_current_username)):
    status['timestamp'] = int(time.time())
    return JSONResponse(content=status)
