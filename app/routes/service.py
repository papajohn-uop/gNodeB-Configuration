
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
service_route_resp["GET"]["start"]="Start 5G Service"
service_route_resp["GET"]["stop"]="Stop 5G service"
service_route_resp["GET"]["restart"]="Restart 5G service"



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

    
@router.get("/start", description="***** Start the 5G service at  the target device*****")
async def system_startService():
    res=common._getConnectionStatus()
    if res:
        res=common._checkCredentials()
        if res:
            checkServiceStatusCMD=common._createCommand("service lte start")
            print(checkServiceStatusCMD)
            process = subprocess.Popen(checkServiceStatusCMD, stdout=subprocess.PIPE)
            out=process.communicate()[0].decode('utf-8')
            rc1=process.returncode
            if rc1==0:
                status="OK"
            else:
                status="NOT OK"
            print(out)
            print(rc1)
            return {"Start Service": status}
        else:
            return {"credentialsVerified": res}
    else:
        return {"connectionStatus": res}


@router.get("/stop", description="***** Stop the 5G service at  the target device*****")
async def system_stopService():
    res=common._getConnectionStatus()
    if res:
        res=common._checkCredentials()
        if res:
            checkServiceStatusCMD=common._createCommand("service lte stop")
            print(checkServiceStatusCMD)
            process = subprocess.Popen(checkServiceStatusCMD, stdout=subprocess.PIPE)
            out=process.communicate()[0].decode('utf-8')
            rc1=process.returncode
            if rc1==0:
                status="OK"
            else:
                status="NOT OK"
            print(out)
            print(rc1)
            return {"Stop Service": status}
        else:
            return {"credentialsVerified": res}
    else:
        return {"connectionStatus": res}



@router.get("/restart", description="***** Restart the 5G service at  the target device*****")
async def system_restartService():
    res=common._getConnectionStatus()
    if res:
        res=common._checkCredentials()
        if res:
            checkServiceStatusCMD=common._createCommand("service lte restart")
            print(checkServiceStatusCMD)
            process = subprocess.Popen(checkServiceStatusCMD, stdout=subprocess.PIPE)
            out=process.communicate()[0].decode('utf-8')
            rc1=process.returncode
            if rc1==0:
                status="OK"
            else:
                status="NOT OK"
            print(out)
            print(rc1)
            return {"restart Service": status}
        else:
            return {"credentialsVerified": res}
    else:
        return {"connectionStatus": res}