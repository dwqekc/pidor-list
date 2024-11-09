from fastapi import WebSocket
from model.wsmanager import ConnectionManager as manager
from model.schemas import InfoPUBSUB

async def pub(pubsub,websocket:WebSocket):
    async for message in pubsub.listen():
        if message["type"] == InfoPUBSUB.type.value:
            await manager.send_message(websocket=websocket,message=message["data"].decode())