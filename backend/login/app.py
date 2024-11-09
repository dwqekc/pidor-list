from fastapi import FastAPI
from login.routers.login import router as login_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(root_path="/api")


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    router=login_router,
    prefix='/login',
)