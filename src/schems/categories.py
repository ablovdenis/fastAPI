from pydantic import BaseModel, Field
from datetime import datetime as dati

class CategoryUpdateAndCreate(BaseModel):
    slug: str = Field(default=None)
    title: str = Field(default=None)
    description: str = Field(default=None)
    is_published: bool = Field(default=None)

class CategoryOut(CategoryUpdateAndCreate):
    id: int
    created_at: dati

    class Config:
        from_attributes = True