
from fastapi import APIRouter

router = APIRouter()

router = APIRouter(
    prefix="/system",
    tags=["system"],
)

@router.get("/",  description="***** SYSTEM COMMANDS ROOT*****")
async def system_root():
    return [{"module": "System related commands"}]

