
from fastapi import APIRouter

router = APIRouter()

router = APIRouter(
    prefix="/system",
    tags=["system"],
)

@router.get("/",  description="***** SYSTEM COMMANDS ROOT*****")
async def system_root():
    return [{"module": "System related commands"}]


@router.get("/CMD1", description="***** SYSTEM COMMAND1 DESCRIPTION*****")
async def system_cmd1():
    return [{"module": "System command 1"}]
