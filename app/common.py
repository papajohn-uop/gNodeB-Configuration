from fastapi import Depends, FastAPI


import ipaddress
import subprocess
import socket

from . import main

def _getConnectionStatus():
    try:
        host = socket.gethostbyname(str(main.ctx.target.IP))
        socket.create_connection((host, 80), 2)
        return True
    except:
        pass
    return False



#CMD_TEMPLATE=["sshpass", "-p", "PASSWORD", "ssh", "-o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no", "USER@IP","CMD"]
CMD_TEMPLATE=["sshpass", "-p", "PASSWORD", "ssh", "-o StrictHostKeyChecking=no ", "USER@IP","CMD"]
#SCREEN_CMD_TEMPLATE=["sshpass", "-p", "PASSWORD", "ssh","-o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no ", "USER@IP","/root/REST_API/api_screen_log.sh", "CMD"]
SCREEN_CMD_TEMPLATE=["sshpass", "-p", "PASSWORD", "ssh","-o StrictHostKeyChecking=no ", "USER@IP","/root/REST_API/api_screen_log.sh", "CMD"]


def _createCommand(cmd):
    myCtx=main.ctx
    tmpCMD=CMD_TEMPLATE
    tmpCMD[2]=myCtx.target.password
    tmpCMD[5]='@'.join([myCtx.target.user,str(myCtx.target.IP)])
    tmpCMD[6]=cmd
    return tmpCMD


def _createScreenCommand(cmd):
    myCtx=main.ctx
    tmpCMD=SCREEN_CMD_TEMPLATE
    tmpCMD[2]=myCtx.target.password
    tmpCMD[5]='@'.join([myCtx.target.user,str(myCtx.target.IP)])
    tmpCMD[7]=cmd
    return tmpCMD


def _checkCredentials():
    checkCredCMD=_createCommand("exit")
    print(checkCredCMD)
    process = subprocess.Popen(checkCredCMD, stdout=subprocess.PIPE)
    out=process.communicate()[0].decode('utf-8')
    rc1=process.returncode
    print(out)
    print(rc1)
    if rc1==255 :
        print("sshpass thnks we have MITM attack")
        print("We should add target to ssh config")
        print("QnD for now")
        rc1=0
        

    return not(rc1)


