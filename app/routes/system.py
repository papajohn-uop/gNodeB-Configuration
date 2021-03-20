
from fastapi import APIRouter
import socket
import subprocess
import ipaddress

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


CHECK_VALIDITY_CMD=["sshpass", "-p", "toor", "ssh", "root@172.16.10.203","exit"]


def _getConnectionStatus():
    try:
        host = socket.gethostbyname(REMOTE_SERVER)
        socket.create_connection((host, 80), 2)
        return True
    except:
        pass
    return False



def _checkCredentials():
    print(CHECK_VALIDITY_CMD)
    process = subprocess.Popen(CHECK_VALIDITY_CMD, stdout=subprocess.PIPE)
    out=process.communicate()[0].decode('utf-8')
    rc1=process.returncode
    print(out)
    print(rc1)
    return not(rc1)


@router.get("/",  description="***** SYSTEM COMMANDS ROOT*****")
async def system_root():
    return system_route_resp

@router.get("/getConnectionStatus", description="***** Checks and returns connection status with target device*****")
async def system_getConnectionStatus():
    res=_getConnectionStatus()
    return {"connectionStatus": res}




@router.get("/checkCredentials", description="***** Checks and returns connection status with target device*****")
async def system_checkCredentials():
    res=_getConnectionStatus()
    if res:
        res=_checkCredentials()
        return {"credentialsVerified": res}
    else:
        return {"connectionStatus": res}
