from fastapi import APIRouter
import socket
import subprocess
import common
from pydantic import BaseModel

router = APIRouter()

router = APIRouter(
    prefix="/screen",
    tags=["screen"],
)


'''
cell             list available cells
ue               show connected UEs
rf_info          Get RF driver informations
tx_gain          get/set the analog TX gain
rx_gain          get/set the analog RX gain
ng               show the NG connection status
time             get UTC and eNB/gNB internal time





cell_gain        set the cell DL gain
tx_gain          get/set the analog TX gain
rx_gain          get/set the analog RX gain
ngconnect        (re)connect to the AMF
ngdisconnect     disconnect from the AMF
quit             Stop eNB/gNB
'''

screen_root_resp=dict()
screen_root_resp["/screen"]="Screen related commands"
screen_root_resp["/screen/CMD1"]="Screen command 1"



screen_root_resp["GET"]=dict()
screen_root_resp["GET"]["getConnectionStatus"]="Check connection status with target device"
screen_root_resp["GET"]["COMMANDS"]=dict()

screen_root_resp["GET"]["COMMANDS"]["cell"]=""
screen_root_resp["GET"]["COMMANDS"]["ue"]=""
screen_root_resp["GET"]["COMMANDS"]["rf_info"]=""
screen_root_resp["GET"]["COMMANDS"]["tx_gain"]=""
screen_root_resp["GET"]["COMMANDS"]["rx_gain"]=""
screen_root_resp["GET"]["COMMANDS"]["ng"]=""

screen_root_resp["GET"]["COMMANDS"]["time"]=""

screen_root_resp["POST"]=dict()
screen_root_resp["POST"]["tx_gain"]=" "
screen_root_resp["POST"]["rx_gain"]=""
screen_root_resp["POST"]["ngconnect"]=""
screen_root_resp["POST"]["ngdisconnect"]=""

REMOTE_SERVER = "172.16.10.203"


@router.get("/", tags=["screen"], description="***** SCREEN COMMANDS ROOT*****")
async def screen_root_get():
    return screen_root_resp

@router.get("/commands", description="***** AVAILABLE SCREEN COMMANDS ROOT*****")
async def screen_commands():
    return (list(screen_root_resp["GET"]["COMMANDS"].keys()))



class gNodeB_GeneralModel(BaseModel):
    path: str
    rc: int
    cmd: str
    output: str


SCREEN_CMD=["sshpass", "-p", "toor", "ssh", "root@172.16.10.203","/root/REST_API/api_screen_log.sh", "CMD"]

@router.get("/commands/{command}", description="***** AVAILABLE SCREEN COMMANDS*****",response_model=gNodeB_GeneralModel)
async def screen_commands(command):
    keys=list(screen_root_resp["GET"]["COMMANDS"].keys())

    print(keys)
    print(command)
    if command in keys:
        res=common._getConnectionStatus()
        if res:
            res=common._checkCredentials()
            if res:
                print("YEAH")
                #setup command
                screenCMD=common._createScreenCommand(command)
                print(screenCMD)
                process = subprocess.Popen(screenCMD, stdout=subprocess.PIPE)
                out=process.communicate()[0].decode('utf-8')
                rc1=process.returncode
                
                data={"path":"SCREEN","rc":rc1,"cmd":command,"output":out}
            else:
                print("CREDENTIALS DO NOT MATCH")
                data={"rc":999,"cmd":command,"output":"Wrong credentials"}
        else:
            print("No Connection")
            data={"rc":999,"cmd":command,"output":"No Connection"}
    else:
        print("OOPS")
        data={"path":"SCREEN","rc":999,"cmd":command,"output":"INVALID COMMAND"}
    
    gnodeB_CMD=gNodeB_GeneralModel(**data)
    return gnodeB_CMD
    