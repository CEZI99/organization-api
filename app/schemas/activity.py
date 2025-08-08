from pydantic import BaseModel
from typing import List, Optional

class ActivityBase(BaseModel):
    name: str
    category: str

class Activity(ActivityBase):
    parent_id: Optional[int] = None
    level: int
    children: List['Activity'] = []

    class Config:
        orm_mode = True  # Ключевая настройка!

# Для избежания циклических импортов
Activity.update_forward_refs()