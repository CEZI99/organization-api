from pydantic import BaseModel
class BaseSchema(BaseModel):
    class Config:
        from_attributes = True  # Ранее orm_mode=True
        use_enum_values = True
