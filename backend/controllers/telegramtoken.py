import jwt
import os
import datetime
from model.core import ModelInterface

SECRET_KEY = os.getenv("SECRET_KEY_JWT")

def tgcreate_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=30)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
    return encoded_jwt    

async def tgget_access_token(userid:str,db):
    try:
        user = await ModelInterface.get_finduser(db=db,userid=userid)
        if not user:  
            raise RuntimeError
        else:
            return user
    except:
        raise RuntimeError