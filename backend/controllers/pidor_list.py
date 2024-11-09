from model.wsmanager import ConnectionManager as manager
from fastapi import WebSocket,HTTPException
from controllers.token import get_access_token,pubsub_time
from model.core import ModelInterface
from functions.helpers.pubsub import pub
import datetime

async def get_pidorWS(websocket:WebSocket,db):
    pubsub = ModelInterface.redis.pubsub()
    try:
        await manager.connect(websocket)
        data = websocket.cookies.get("Authorization")
        await get_access_token(data,db)          
        await pubsub.subscribe("fagots")
        await pub(pubsub=pubsub,websocket=websocket)
    except:
        await pubsub.unsubscribe("fagots")
        await manager.disconnect(websocket)


async def set_pidorWS(websocket:WebSocket,db):
    try:
        await manager.connect(websocket)
        data = websocket.cookies.get("Authorization")
        await get_access_token(data,db) 
    except:
        await manager.disconnect(websocket)  
    try:    
        while True:
            msg = await websocket.receive_text()
            if isinstance(msg,str):
                user = await pubsub_time(data,db)
                #if datetime.datetime.now(datetime.timezone.utc) >= user.last_activity + datetime.timedelta(seconds=InfoAccount.delay.value):
                await ModelInterface.set_pub(data=data,fagot=int(msg),db=db)
                user.last_activity = datetime.datetime.now(datetime.timezone.utc)
                await db.commit()
    except:
        await manager.disconnect(websocket)

    
async def get_pidor(Authorization,db,amount:int,offset:int):
    try:
        await get_access_token(Authorization,db)
        data = await ModelInterface.get_pidor(db=db,amount=amount,offset=offset)
        return data
    except:
        raise HTTPException(status_code=422)

