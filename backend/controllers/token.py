import jwt
import os
from controllers.googletoken import get_access_token as google_access
from controllers.telegramtoken import tgget_access_token
from model.core import ModelInterface
from model.schemas import TypeAuth

SECRET_KEY = os.getenv("SECRET_KEY_JWT")

async def get_access_token(token:str,db):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        decode_type: str = payload.get('type')
        if decode_type == TypeAuth.google.value:
            decode_token: str = payload.get('token')
            id_info = google_access(decode_token)
            if not await ModelInterface.get_finduser(db=db,email=id_info.get("email")):
                raise RuntimeError
            return id_info
        if decode_type == TypeAuth.telegram.value:
            decode_userid: str = payload.get('userid')
            user = await tgget_access_token(userid=decode_userid,db=db)
            return user
    except:
        raise RuntimeError

async def pubsub_time(token:str,db):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        decode_type: str = payload.get('type')
        if decode_type == TypeAuth.google.value:
            decode_token: str = payload.get('token')
            id_info = google_access(decode_token)
            user = await ModelInterface.get_finduser(db=db,email=id_info.get("email"))
            if not user:
                raise RuntimeError
            return user
        if decode_type == TypeAuth.telegram.value:
            decode_userid: str = payload.get('userid')
            user = await ModelInterface.get_finduser(db=db,userid=decode_userid)
            if not user: 
                raise RuntimeError
            return user
    except:
        raise RuntimeError