from pydantic import BaseModel, Field, EmailStr
from datetime import datetime as dati

class UserUpdate(BaseModel):
    first_name: str = Field(default=None)
    last_name: str = Field(default=None)
    bio_info: str = Field(default=None)
    email: EmailStr = Field(default=None)

class UserCreate(UserUpdate):
    nickname: str
    password: str

class UserOut(UserUpdate):
    id: int
    nickname: str
    active: bool
    date_joined: dati

    class Config:
        from_attributes = True