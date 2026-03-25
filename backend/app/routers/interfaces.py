from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
import models

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
