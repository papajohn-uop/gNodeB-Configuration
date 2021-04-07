from fastapi import Depends, FastAPI
from app.routes import  system, service ,ws, screen

import ipaddress
import subprocess
import socket

app = FastAPI()


app.include_router(system.router)
app.include_router(service.router)
app.include_router(ws.router)
app.include_router(screen.router)

class Target:
    def __init__(self,user=None, password=None, IP=None):
        self.description="Some desc"
        if user is None:
            self.user=None
        else:
            self.user= user

        if password is None:
            self.password=None
        else:
            self.password= password
    
    def setUser(self,user):
        self.user=user

    def setPass(self,password):
        self.password=password

    def setIP(self,IP):
        self.IP= ipaddress.ip_address(IP)


class Context:
    def __init__(self,target=None):
        self.self_info="Server info"
        if target is None:
            self.target=None
        else:
            self.target= target
  
    def setTarget(self,target):
        self.target= target



ctx=None


def populateContext():
    global ctx
    if ctx is None:
        target=Target()
        target.setIP("172.16.10.203")
        target.setUser("root")
        target.setPass("toor")
        ctx=Context(target)

    
    print(ctx.target.IP)

@app.on_event("startup")
async def startup_event():
    print("Startup")
    populateContext()
    

    ctx=Context()
    if ctx.target:
        if ctx.target.credentials:
            if ctx.target.credentials.user:
                print(ctx.target.credentials.user)
   

main_resp=dict()
main_resp["/system"]="System related commands"
main_resp["/service"]="Service related commands"
main_resp["/ws"]="WebSockets related commands"
main_resp["/screen"]="Screen related commands"


@app.get("/")
async def root():
    return main_resp





