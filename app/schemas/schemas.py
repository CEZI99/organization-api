from pydantic import BaseModel
from typing import List, Optional

class PhoneBase(BaseModel):
    phone: str

class PhoneCreate(PhoneBase):
    pass

class Phone(PhoneBase):
    id: int
    class Config:
        orm_mode = True

class ActivityBase(BaseModel):
    name: str
    parent_id: Optional[int] = None

class ActivityCreate(ActivityBase):
    pass

class Activity(ActivityBase):
    id: int
    children: List['Activity'] = []
    class Config:
        orm_mode = True

class BuildingBase(BaseModel):
    address: str
    latitude: float
    longitude: float

class BuildingCreate(BuildingBase):
    pass

class Building(BuildingBase):
    id: int
    class Config:
        orm_mode = True

class OrganizationBase(BaseModel):
    name: str
    building_id: int

class OrganizationCreate(OrganizationBase):
    phones: List[PhoneBase] = []
    activity_ids: List[int] = []

class Organization(OrganizationBase):
    id: int
    phones: List[Phone] = []
    activities: List[Activity] = []
    building: Building
    class Config:
        orm_mode = True