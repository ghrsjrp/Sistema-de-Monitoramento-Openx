from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

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


class Link(Base):
    __tablename__ = "links"

    id = Column(Integer, primary_key=True, index=True)

    local_device_id = Column(Integer)
    local_port = Column(String)

    remote_device_name = Column(String)
    remote_port = Column(String)
