from pydantic import BaseModel
from typing import List, Optional

class InterfaceBase(BaseModel):
    name: str
    description: Optional[str] = None
    status: Optional[str] = "down"

class InterfaceCreate(InterfaceBase):
    pass

class Interface(InterfaceBase):
    id: int

    class Config:
        from_attributes = True


class DeviceBase(BaseModel):
    hostname: str
    ip: str
    vendor: Optional[str] = None
    model: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    snmp_community: Optional[str] = None
    snmp_version: Optional[str] = "2c"

class DeviceCreate(DeviceBase):
    interfaces: List[InterfaceCreate] = []

class Device(DeviceBase):
    id: int
    interfaces: List[Interface] = []

    class Config:
        from_attributes = True


class LinkBase(BaseModel):
    local_device_id: int
    local_port: str
    remote_device_name: str
    remote_port: str

class LinkCreate(LinkBase):
    pass

class Link(LinkBase):
    id: int

    class Config:
        from_attributes = True
