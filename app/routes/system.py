
from fastapi import APIRouter
import socket
import subprocess
import ipaddress
import main


router = APIRouter()

router = APIRouter(
    prefix="/system",
    tags=["system"],
)

system_route_resp=dict()
system_route_resp["Module"]="Websocket related commands"
system_route_resp["GET"]=dict()
system_route_resp["GET"]["getConnectionStatus"]="Check connection status with target device"



CMD_TEMPLATE=["sshpass", "-p", "PASSWORD", "ssh", "USER@IP","CMD"]



def _getConnectionStatus():
    print(main.ctx.target.IP)
    try:
        host = socket.gethostbyname(str(main.ctx.target.IP))
        socket.create_connection((host, 80), 2)
        return True
    except:
        pass
    return False




def _createCommand(cmd):
    myCtx=main.ctx
    tmpCMD=CMD_TEMPLATE
    tmpCMD[2]=myCtx.target.password
    tmpCMD[4]='@'.join([myCtx.target.user,str(myCtx.target.IP)])
    tmpCMD[5]="exit"
    return tmpCMD

def _checkCredentials():
    checkCredCMD=_createCommand("exit")
    process = subprocess.Popen(checkCredCMD, stdout=subprocess.PIPE)
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
