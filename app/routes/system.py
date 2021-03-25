
from fastapi import APIRouter
import socket
import subprocess
import ipaddress
from .. import common


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
system_route_resp["GET"]["configurations"]="Change configuration "
system_route_resp["GET"]["get_conf"]="Download conf from github repo"


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



system_configurations=dict()

system_configurations["conf1"]=dict()
system_configurations["conf1"]["file"]="gnb-sa-TDD3-Open5GS.cfg"
system_configurations["conf1"]["Desc"]="Configuration1 with parameters ....."

system_configurations["conf2"]=dict()
system_configurations["conf2"]["file"]="gnb-sa-TDD3-40MHz.cfg"
system_configurations["conf2"]["Desc"]="Configuration2 with parameters ....."

system_configurations["conf3"]=dict()
system_configurations["conf3"]["file"]="gnb-sa-TDD2-40MHz.cfg"
system_configurations["conf3"]["Desc"]="Configuration3 with parameters ....."

system_configurations["conf4"]=dict()
system_configurations["conf4"]["file"]="gnb-sa-TDD2.cfg"
system_configurations["conf4"]["Desc"]="Configuration4 with parameters ....."

system_configurations["conf5"]=dict()
system_configurations["conf5"]["file"]="gnb-sa-TDD3.cfg"
system_configurations["conf5"]["Desc"]="Configuration5 with parameters ....."


@router.get("/configurations", description="***** AVAILABLE CONFIGURATIONS ROOT*****")
async def system_Configurations():
    return ((system_configurations)  )  


@router.get("/configurations/{conf}", description="***** CHANGE CONFIGURATION*****")
async def change_configuration(conf):
    keys=list(system_configurations.keys())

    print(keys)
    print(conf)
    if conf in keys:
        res=common._getConnectionStatus()
        if res:
            res=common._checkCredentials()
            if res:
                print("YEAH")
                print(system_configurations[conf]["file"])
                #Change symbolic link target 
                cmd=common._createCommand(''.join(["ln -sf ",system_configurations[conf]["file"], " /root/enb/config/enb.cfg"]))
                print(cmd)
                process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
                out=process.communicate()[0].decode('utf-8')
                rc1=process.returncode
                print(rc1)
                #ln -sf gnb-sa-TDD3.cfg enb.cfg
                #restart service
                if not rc1:
                    if res:
                        restartServiceCMD=common._createCommand("service lte restart")
                        #print(checkServiceStatusCMD)
                        process = subprocess.Popen(restartServiceCMD, stdout=subprocess.PIPE)
                        out=process.communicate()[0].decode('utf-8')
                        rc1=process.returncode
                        if rc1==0:
                            return{"Service restarted with conf:": system_configurations[conf]["file"]}
                        else:
                            return{"Service restart failed": out}

            else:
                return {"credentialsVerified": res}
        else:
            return {"connectionStatus": res}
    else:
        print("OOPS")
        return {"status": "Invalid Conf"}
    
   


@router.get("/get_conf/{conf}", description="***** CHANGE CONFIGURATION*****")
async def get_conf(conf):
    print(conf)
    res=common._getConnectionStatus()
    if res:
        res=common._checkCredentials()
        if res:
            print("YEAH")
            #download target
            cmd=common._createCommand(''.join(["wget ","https://raw.githubusercontent.com/papajohn-uop/gNodeB-Configuration/main/configuration_files/",conf ," -P /root/enb/config/"]))
            print(cmd)
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
            out=process.communicate()[0].decode('utf-8')
            rc1=process.returncode
            print(rc1)
            if not rc1: #which means that we found and dwonloaded the file
                #Change symbolic link target 
                cmd=common._createCommand(''.join(["ln -sf ",conf, " /root/enb/config/enb.cfg"]))
                print(cmd)
                process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
                out=process.communicate()[0].decode('utf-8')
                rc1=process.returncode
                print(rc1)
                #ln -sf gnb-sa-TDD3.cfg enb.cfg
                #restart service
                if not rc1:
                    if res:
                        restartServiceCMD=common._createCommand("service lte restart")
                        #print(checkServiceStatusCMD)
                        process = subprocess.Popen(restartServiceCMD, stdout=subprocess.PIPE)
                        out=process.communicate()[0].decode('utf-8')
                        rc1=process.returncode
                        if rc1==0:
                            return{"Service restarted with conf:": conf}
                        else:
                            return{"Service restart failed": out}
            else:
                return{"File not found": conf}

        else:
            return {"credentialsVerified": res}
    else:
        return {"connectionStatus": res}
