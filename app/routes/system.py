
from fastapi import APIRouter
import socket

router = APIRouter()

router = APIRouter(
    prefix="/system",
    tags=["system"],
)

system_route_resp=dict()
system_route_resp["Module"]="Websocket related commands"
system_route_resp["GET"]=dict()
system_route_resp["GET"]["getConnectionStatus"]="Check connection status with target device"

REMOTE_SERVER = "172.16.10.203"

def _getConnectionStatus():
    try:
        host = socket.gethostbyname(REMOTE_SERVER)
        socket.create_connection((host, 80), 2)
        return True
    except:
        pass
    return False


@router.get("/",  description="***** SYSTEM COMMANDS ROOT*****")
async def system_root():
    return system_route_resp

@router.get("/getConnectionStatus", description="***** Checks and returns connection status with target device*****", response_model=bool)
async def ws_getConnectionStatus():
        return _getConnectionStatus()
