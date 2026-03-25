from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models
from app.services.lldp import get_lldp_neighbors

router = APIRouter(prefix="/lldp", tags=["LLDP"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/discover/{device_id}")
def discover_lldp(device_id: int, db: Session = Depends(get_db)):
    device = db.query(models.Device).filter(models.Device.id == device_id).first()

    if not device:
        return {"error": "Device not found"}

    neighbors = get_lldp_neighbors(device.ip, device.snmp_community)

    count = 0

    for n in neighbors:
        link = models.Link(
            local_device_id=device.id,
            local_port=n["local_port"],
            remote_device_name=n["remote_device"],
            remote_port=n["remote_port"]
        )
        db.add(link)
        count += 1

    db.commit()

    return {
        "status": "ok",
        "neighbors_found": len(neighbors),
        "links_saved": count
    }


@router.get("/")
def list_links(db: Session = Depends(get_db)):
    return db.query(models.Link).all()
