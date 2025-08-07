from pydantic import BaseModel
from typing import List
from datetime import datetime
from .building import Building
from .activity import Activity


class PhoneBase(BaseModel):
    number: str

class PhoneCreate(PhoneBase):
    pass

class Phone(PhoneBase):
    id: int
    organization_id: int

    class Config:
        from_attributes = True

class OrganizationBase(BaseModel):
    name: str
    building_id: int

class OrganizationCreate(OrganizationBase):
    activity_ids: List[int] = []
    phones: List[PhoneCreate] = []

class Organization(OrganizationBase):
    id: int
    building: Building
    activities: List[Activity] = []
    phones: List[Phone] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
