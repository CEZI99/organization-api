from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class PhoneBase(BaseModel):
    number: str

class Phone(PhoneBase):
    id: int
    organization_id: int

    class Config:
        orm_mode = True

class BuildingBase(BaseModel):
    address: str
    latitude: float
    longitude: float

class Building(BuildingBase):
    id: int

    class Config:
        orm_mode = True

class ActivityBase(BaseModel):
    name: str
    category: str

class ActivitySimple(ActivityBase):
    id: int
    parent_id: Optional[int] = None

    class Config:
        orm_mode = True

class OrganizationBase(BaseModel):
    name: str
    building_id: int

    class Config:
        orm_mode = True

class OrganizationFull(OrganizationBase):
    id: int
    building: Building
    activities: List[ActivitySimple] = []
    phones: List[Phone] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class BuildingInRect(BaseModel):
    address: str

    class Config:
        orm_mode = True


class Activity(ActivitySimple):
    children: List['Activity'] = []

    class Config:
        orm_mode = True

class ActivityWithLevel(ActivityBase):
    id: int
    level: int
    parent_id: Optional[int] = None

    class Config:
        orm_mode = True

class OrganizationWithActivities(OrganizationBase):
    id: int
    building: Building
    activities: List[ActivityWithLevel] = []

    class Config:
        orm_mode = True


class OrganizationWithBuilding(OrganizationBase):
    building: Building

Activity.update_forward_refs()
