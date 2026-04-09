from typing import List, Type

from fastapi import HTTPException
from sqlalchemy.orm import Session

from ..models.user_models import UserModel
from ....schems.users import UserCreate, UserUpdate


class UserRepository:
    def __init__(self):
        pass

    def get(self, DataBase: Session, skip: int, limit: int) -> List[UserModel]:
        return DataBase.query(UserModel).offset(skip).limit(limit).all()

    def get_detail(self, DataBase: Session, nickname: str) -> UserModel:
        user = DataBase.query(UserModel).filter(UserModel.nickname == nickname).first()
        if not user:
            raise HTTPException(status_code=404, detail='Пользователя не существует.')
        return user

    def create(self, DataBase: Session, payload: UserCreate) -> UserModel:
        existing = DataBase.query(UserModel).filter(
            (UserModel.nickname == payload.nickname) |
            (UserModel.email == payload.email)
        ).first()
        if existing:
            raise HTTPException(
                status_code=400,
                detail='Пользователь с такими никнеймом и почтой уже существует.'
            )
        user = UserModel(
            nickname=payload.nickname,
            email=payload.email,
            first_name=payload.first_name,
            last_name=payload.last_name,
            bio_info=payload.bio_info,
            password=payload.password,
        )
        DataBase.add(user)
        DataBase.commit()
        DataBase.refresh(user)
        return user

    def update(self, DataBase: Session, nickname: str, payload: UserUpdate) -> UserModel:
        user = DataBase.query(UserModel).filter(UserModel.nickname == nickname).first()
        if not user:
            raise HTTPException(status_code=404, detail='Пользователь не существует.')
        update_data = payload.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user, field, value)
        DataBase.commit()
        DataBase.refresh(user)
        return user

    def destroy(self, DataBase: Session, nickname: str):
        user = DataBase.query(UserModel).filter(UserModel.nickname == nickname).first()
        if not user:
            raise HTTPException(status_code=404, detail='Пользователь не существует.')
        DataBase.delete(user)
        DataBase.commit()