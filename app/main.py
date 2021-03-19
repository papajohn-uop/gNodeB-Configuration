from fastapi import Depends, FastAPI
from routes import  system 


app = FastAPI()


app.include_router(system.router)

main_resp=dict()
main_resp["/system"]="System related commands"

@app.get("/")
async def root():
    return main_resp

