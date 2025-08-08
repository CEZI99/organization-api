from pydantic import BaseModel

class BuildingBase(BaseModel):
    address: str
    latitude: float
    longitude: float

class Building(BuildingBase):
    id: int

    class Config:
        orm_mode = True  # Ключевая настройка!
