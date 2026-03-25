from fastapi import FastAPI
from app.database import engine, Base
from app.routers import devices, interfaces

Base.metadata.create_all(bind=engine)

app = FastAPI(title="NetMon API")

app.include_router(devices.router)
app.include_router(interfaces.router)
