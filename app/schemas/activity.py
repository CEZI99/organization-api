from pydantic import BaseModel
from typing import List, Optional

class ActivityBase(BaseModel):
    name: str
    category: str

class ActivityCreate(ActivityBase):
    parent_id: Optional[int] = None

class Activity(ActivityBase):
    id: int
    parent_id: Optional[int]
    children: List['Activity'] = []
    
    class Config:
        from_attributes = True

# Для избежания циклических импортов
Activity.update_forward_refs()