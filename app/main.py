from fastapi import FastAPI
from app.v1.routes import router

app = FastAPI()

app.include_router(router=router)