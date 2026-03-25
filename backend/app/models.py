from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    hostname = Column(String)
    ip = Column(String, unique=True)
    vendor = Column(String)
    model = Column(String)
    username = Column(String)
    password = Column(String)
    snmp_community = Column(String)
    snmp_version = Column(String)

    interfaces = relationship("Interface", back_populates="device", cascade="all, delete")


class Interface(Base):
    __tablename__ = "interfaces"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    status = Column(String)

    device_id = Column(Integer, ForeignKey("devices.id"))
    device = relationship("Device", back_populates="interfaces")
