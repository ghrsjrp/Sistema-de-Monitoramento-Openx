from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models, schemas
from app.services.snmp import get_interfaces

router = APIRouter(prefix="/devices", tags=["Devices"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=list[schemas.Device])
def list_devices(db: Session = Depends(get_db)):
    return db.query(models.Device).all()


@router.post("/{device_id}/discover")
def discover_device(device_id: int, db: Session = Depends(get_db)):
    device = db.query(models.Device).filter(models.Device.id == device_id).first()

    if not device:
        return {"error": "Device not found"}

    interfaces = get_interfaces(device.ip, device.snmp_community)

    count = 0

    for iface in interfaces:
        exists = db.query(models.Interface).filter_by(
            device_id=device.id,
            name=iface["name"]
        ).first()

        if not exists:
            new_iface = models.Interface(
                name=iface["name"],
                description=iface["description"],
                status="unknown",
                device_id=device.id
            )
            db.add(new_iface)
            count += 1

    db.commit()

    return {
        "status": "ok",
        "interfaces_found": len(interfaces),
        "interfaces_added": count
    }


