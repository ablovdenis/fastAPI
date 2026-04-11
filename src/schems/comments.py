from pydantic import BaseModel, Field
from datetime import datetime as dati


class CommentUpdate(BaseModel):
    text: str = Field(default=None)

class CommentCreate(CommentUpdate):
    post_id: int
    author_nickname: str

class CommentOut(CommentUpdate):
    post_id: int
    author_id: int
    id: int
    created_at: dati

    class Config:
        from_attributes = True