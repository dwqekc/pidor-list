from fastapi import APIRouter,Cookie,HTTPException,WebSocket,Depends
from sqlalchemy.ext.asyncio import AsyncSession as Session
from model.core import ModelInterface
from controllers.pidor_list import get_pidor,get_pidorWS,set_pidorWS
from typing import Annotated,Union

router = APIRouter()

@router.get("/all_pidor")
async def all_pidor(amount: int,offset: int, db: Session = Depends(ModelInterface.get_db),Authorization: Annotated[Union[str, None], Cookie()] = None):
    if Authorization:
        data = await get_pidor(Authorization,db=db,amount=amount,offset=offset)
        return data
    else:
        raise HTTPException(status_code=422)

@router.websocket("/getpidor")
async def websocket_endpoint(websocket: WebSocket,db: Session = Depends(ModelInterface.get_db)):
    await get_pidorWS(websocket,db=db)

@router.websocket("/setpidor")
async def websocket_endpoint(websocket: WebSocket,db: Session = Depends(ModelInterface.get_db)):
    await set_pidorWS(websocket,db=db)