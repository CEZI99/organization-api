from pydantic import BaseModel
from typing import List
from datetime import datetime
from .building import Building
from .activity import Activity


class PhoneBase(BaseModel):
    number: str

class Phone(PhoneBase):
    organization_id: int

    class Config:
        orm_mode = True

class OrganizationBase(BaseModel):
    name: str
    building_id: int

    class Config:
        orm_mode = True  # Ключевая настройка!

class OrganizationFull(BaseModel):
    id: int
    name: str
    building: Building  # Измените на один объект, а не список
    activities: List[Activity] = []
    phones: List[Phone] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class Organization(BaseModel):
    name: str

    class Config:
        orm_mode = True  # Ключевая настройка!
