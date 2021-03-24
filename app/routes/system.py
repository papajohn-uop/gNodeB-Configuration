
from fastapi import APIRouter
import socket
import subprocess
import ipaddress
import common


router = APIRouter()

router = APIRouter(
    prefix="/system",
    tags=["system"],
)

system_route_resp=dict()
system_route_resp["Module"]="System related commands"
system_route_resp["GET"]=dict()
system_route_resp["GET"]["getConnectionStatus"]="Check connection status with target device"
system_route_resp["GET"]["checkCredentials"]="Check targets device credentials"



@router.get("/",  description="***** SYSTEM COMMANDS ROOT*****")
async def system_root():
    return system_route_resp

@router.get("/getConnectionStatus", description="***** Checks and returns connection status with target device*****")
async def system_getConnectionStatus():
    res=common._getConnectionStatus()
    return {"connectionStatus": res}




@router.get("/checkCredentials", description="***** Checks and returns connection status with target device*****")
async def system_checkCredentials():
    res=common._getConnectionStatus()
    if res:
        res=common._checkCredentials()
        return {"credentialsVerified": res}
    else:
        return {"connectionStatus": res}



    
