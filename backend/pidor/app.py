from fastapi import FastAPI
from pidor.routers.pidor_list import router as pidor_router
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
    router=pidor_router,
    prefix='/pidor',
)