from fastapi import APIRouter
import socket
import subprocess
from pydantic import BaseModel
import common
from websocket import create_connection

router = APIRouter()

router = APIRouter(
    prefix="/ws",
    tags=["websocket"],
)


REMOTE_SERVER = "172.16.10.203"

ws_root_resp=dict()
ws_root_resp["Module"]="Websocket related commands"
ws_root_resp["GET"]=dict()
ws_root_resp["GET"]["getConnectionStatus"]="Check connection status with target device"
ws_root_resp["GET"]["COMMANDS"]=dict()

ws_root_resp["GET"]["COMMANDS"]["config_get"]="Get configuration"
ws_root_resp["GET"]["COMMANDS"]["ue_get"]="Get UE info"
ws_root_resp["GET"]["COMMANDS"]["geteRab"]="Get bearer info"
ws_root_resp["GET"]["COMMANDS"]["qos_flow_get"]="Get qos info"
ws_root_resp["GET"]["COMMANDS"]["rf"]="Get RF info"
ws_root_resp["GET"]["COMMANDS"]["stats"]="Get statistics from/for the gNodeB "
ws_root_resp["GET"]["COMMANDS"]["ng"]="Get ng status "


ws_root_resp["POST"]=dict()
ws_root_resp["POST"]["ngconnect"]=" "
ws_root_resp["POST"]["ngdisconnect"]=""
ws_root_resp["POST"]["ngadd"]=""
ws_root_resp["POST"]["ngdelete"]=""
'''
    #POST TODO     "config_set",
    #POST   TODO     "ngconnect",
    #POST    TODO"ngdisconnect",
    #POST  TODO     "ngadd",
    #POST TODO      "ngdelete",

'''

def _getConnectionStatus():
    try:
        host = socket.gethostbyname(REMOTE_SERVER)
        socket.create_connection((host, 80), 2)
        return True
    except:
        pass
    return False






@router.get("/", description="***** WEBSOCKET COMMANDS ROOT*****")
async def ws_root_get():

    return ws_root_resp


WS_GNODEB=["./routes/ws.js", "172.16.10.203:9001","CMD"]

class gNodeB_GeneralModel(BaseModel):
    rc: int
    cmd: str
    output: str



@router.get("/commands", description="***** AVAILABLE WEBSOCKET COMMANDS ROOT*****")
async def ws_commands():
    return (list(ws_root_resp["GET"]["COMMANDS"].keys()))

@router.get("/commands/{command}", description="***** AVAILABLE WEBSOCKET COMMANDS*****",response_model=gNodeB_GeneralModel)
async def ws_commands(command):
    keys=list(ws_root_resp["GET"]["COMMANDS"].keys())

    print(keys)

    if command in keys:
        res=common._getConnectionStatus()
        if res:
            res=common._checkCredentials()
            if res:
                print("YEAH")
                #setup command
                ws = create_connection("ws://172.16.10.203:9001/")
                print("Sending 'Hello, World'...")
                cmd="".join(["{\"message\": \"",command,"\"}"])
                ws.send(cmd)
                print("Sent")
                print("Receiving...")
                result =  ws.recv()
                print("Received '%s'" % result)
                result =  ws.recv()
                print("Received '%s'" % result)
                ws.close()
                data={"rc":0,"cmd":command,"output":result}
            else:
                print("CREDENTIALS DO NOT MATCH")
                data={"rc":999,"cmd":command,"output":"Wrong credentials"}
        else:
            print("No Connection")
            data={"rc":999,"cmd":command,"output":"No Connection"}
    else:
        print("OOPS")
        data={"rc":999,"cmd":command,"output":"INVALID COMMAND"}
    
    gnodeB_CMD=gNodeB_GeneralModel(**data)
    
    
    
    return gnodeB_CMD
    
