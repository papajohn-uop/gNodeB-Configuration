from fastapi import Depends, FastAPI


app = FastAPI()



@app.get("/")
async def root():
    return {"message": "Amarisoft gNodeB configuration!"}

