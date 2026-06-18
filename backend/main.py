from fastapi import FastAPI
from src.routes import base_router,data_router
from src.config import connect_mongodb
app=FastAPI()

connect_mongodb()

app.include_router(base_router)
app.include_router(data_router)
