from pydantic import BaseModel, Field, EmailStr, field_validator
from fastapi import HTTPException, status
from datetime import datetime as dati
import re

def valid_first_or_last_name(name: str, meaning: str) -> str:
    len_name = len(name)
    if len_name < 2 or len_name >= 31:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=f'{meaning} должно состоять хотя бы из 2 букв и быть не длинее 30 символов.'
        )
    if not re.match(r'^[а-яёА-ЯЁa-zA-Z]+$', name):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=f'{meaning} должно состоять только из букв латинского алфавита или кириллицы.'
        )
    if not re.match(r'[A-ZА-ЯЁ]', name[0]):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=f'{meaning} должно начинаться с заглавной буквы.'
        )
    if not re.match(r'^.[а-яёa-z]+$', name):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=f'{meaning} может только начинаться с заглавной буквы.'
        )
    return name


def valid_nickname(nickname: str):
    len_nickname = len(nickname)
    if len_nickname < 3 or len_nickname > 30:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail='Никнейм должен быть длиннее 2 символов и короче 21 символа.'
        )
    return nickname


class UserUpdate(BaseModel):
    first_name: str = Field()
    last_name: str = Field()
    bio_info: str = Field()
    email: EmailStr = Field()

    @field_validator("first_name", mode="after")
    @staticmethod
    def check_first_name(first_name: str):
        return valid_first_or_last_name(first_name, 'Имя')

    @field_validator("last_name", mode="after")
    @staticmethod
    def check_last_name(last_name: str):
        return valid_first_or_last_name(last_name, 'Фамилия')


class UserCreate(UserUpdate):
    nickname: str = Field(min_length=3, max_length=20)
    password: str = Field(min_length=9, max_length=30)

    @field_validator("nickname", mode="after")
    @staticmethod
    def check_nickname(nickname: str):
        return valid_nickname(nickname)

    @field_validator("password", mode="after")
    @staticmethod
    def check_password(password: str):
        len_password = len(password)
        if password < 10 or len_password > 100:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail='Пароль должен быть длиннее 9 символов и короче 101 символа.'
            )
        return password


class UserOut(UserUpdate):
    id: int
    nickname: str
    active: bool
    date_joined: dati

    @field_validator("nickname", mode="after")
    @staticmethod
    def check_nickname(nickname: str):
        return valid_nickname(nickname)

    class Config:
        from_attributes = True