from fastapi import Request,APIRouter,Depends
from sqlalchemy.ext.asyncio import AsyncSession as Session
from fastapi.responses import RedirectResponse
from controllers.googletoken import create_access_token,create_link
from controllers.telegramtoken import tgcreate_access_token
from model.schemas import TypeAuth
from model.core import ModelInterface
import os
import datetime
router = APIRouter()

@router.get("/google")
async def login_google():
    authorization_url = create_link()
    return {"google_url":authorization_url}

@router.get("/callback")
async def google_callback(request:Request,db: Session = Depends(ModelInterface.get_db)):
    Authorization,expires = await create_access_token(request,db)
    response = RedirectResponse(os.getenv("REDIRECT_APP"))
    response.set_cookie(key="Authorization", value=Authorization,expires=expires,domain=os.getenv("DOMAIN_COOKIE"))
    return response

@router.get("/tgcallback")
async def telegram_callback(request:Request,db: Session = Depends(ModelInterface.get_db)):
    query_params = request.query_params
    if not await ModelInterface.get_finduser(db=db,userid=str(query_params.get("id"))): 
        await ModelInterface.set_user(db=db,type=TypeAuth.telegram.value,userid=str(query_params.get("id")),username=query_params.get("username"),first_name=query_params.get("first_name"),last_name=query_params.get("last_name"),photo_url=query_params.get("photo_url"))
    Authorization = tgcreate_access_token({"type":"telegram","userid":query_params.get("id")})
    response = RedirectResponse(os.getenv("REDIRECT_APP"))
    response.set_cookie(key="Authorization", value=Authorization,expires=datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=30),domain=os.getenv("DOMAIN_COOKIE"))
    return response
