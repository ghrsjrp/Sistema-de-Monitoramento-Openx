from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
import models, schemas

router = APIRouter(prefix="/devices", tags=["Devices"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def create_device(device: schemas.DeviceCreate, db: Session = Depends(get_db)):
    db_device = models.Device(**device.dict(exclude={"interfaces"}))
    db.add(db_device)
    db.commit()
    db.refresh(db_device)

    for iface in device.interfaces:
        db_iface = models.Interface(**iface.dict(), device_id=db_device.id)
        db.add(db_iface)

    db.commit()

    return db_device


@router.get("/")
def list_devices(db: Session = Depends(get_db)):
    return db.query(models.Device).all()


@router.delete("/{device_id}")
def delete_device(device_id: int, db: Session = Depends(get_db)):
    device = db.query(models.Device).get(device_id)
    if device:
        db.delete(device)
        db.commit()
    return {"status": "deleted"}
