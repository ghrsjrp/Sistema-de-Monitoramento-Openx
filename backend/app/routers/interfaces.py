from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models

router = APIRouter(prefix="/interfaces", tags=["Interfaces"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def list_interfaces(db: Session = Depends(get_db)):
    return db.query(models.Interface).all()


@router.get("/{device_id}")
def list_device_interfaces(device_id: int, db: Session = Depends(get_db)):
    return db.query(models.Interface).filter(models.Interface.device_id == device_id).all()
