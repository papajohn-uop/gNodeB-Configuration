
from fastapi import APIRouter
import socket
import subprocess
import ipaddress
import common



router = APIRouter()

router = APIRouter(
    prefix="/service",
    tags=["system"],
)

service_route_resp=dict()
service_route_resp["Module"]="Service related commands"
service_route_resp["GET"]=dict()
service_route_resp["GET"]["checkServiceStatus"]="checkServiceStatus"



@router.get("/",  description="***** SERVICE COMMANDS ROOT*****")
async def service_root():
    return service_route_resp

@router.get("/checkServiceStatus", description="***** Checks and returns service status on the target device*****")
async def system_ServiceStatus():
    res=common._getConnectionStatus()
    if res:
        res=common._checkCredentials()
        if res:
            checkServiceStatusCMD=common._createCommand(" systemctl is-active  lte")
            print(checkServiceStatusCMD)
            process = subprocess.Popen(checkServiceStatusCMD, stdout=subprocess.PIPE)
            out=process.communicate()[0].decode('utf-8')
            rc1=process.returncode
            print(out)
            print(rc1)
            return {"serviceStatus": out.strip('\n')}
        else:
            return {"credentialsVerified": res}
    else:
        return {"connectionStatus": res}

    
