from pydantic import BaseModel, Field
from datetime import datetime as dati
from typing import List

from .users import UserOut
from .categories import CategoryOut
from .locations import LocationOut
from .comments import CommentOut

class PostUpdate(BaseModel):
    title: str = Field(default=None)
    text: str = Field(default=None)
    pub_date: dati = Field(default=None)
    is_published: bool = Field(default=None)
    image: str = Field(default=None)
    location_name: str = Field(default=None)
    category_slug: str = Field(default=None)

class PostCreate(PostUpdate):
    author_nickname: str = Field(default=None)

class PostOut(BaseModel):
    id: int
    created_at: dati
    title: str = Field(default=None)
    text: str = Field(default=None)
    pub_date: dati = Field(default=None)
    is_published: bool = Field(default=None)
    image: str = Field(default=None)
    location_id: int = Field(default=None)
    category_id: int = Field(default=None)
    author_id: int = Field(default=None)

    class Config:
        from_attributes = True

class PostDetail(PostOut):
    author: UserOut
    category: CategoryOut = Field(default=None)
    location: LocationOut = Field(default=None)
    comments: List["CommentOut"] = Field(default=[])

    class Config:
        from_attributes = True