from pydantic import BaseModel, Field, EmailStr
from datetime import datetime as dati

class UserUpdate(BaseModel):
    first_name: str = Field()
    last_name: str = Field()
    bio_info: str = Field()
    email: EmailStr = Field()

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