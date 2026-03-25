from fastapi import FastAPI
from app.database import engine
from app import models
from app.routers import devices, interfaces, lldp

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(devices.router)
app.include_router(interfaces.router)
app.include_router(lldp.router)
