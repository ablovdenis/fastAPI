from pydantic import BaseModel, Field
from datetime import datetime as dati


class LocationUpdateAndCreate(BaseModel):
    name: str = Field(default=None)
    is_published: bool = Field(default=None)

class LocationOut(LocationUpdateAndCreate):
    id: int
    created_at: dati

    class Config:
        from_attributes = True