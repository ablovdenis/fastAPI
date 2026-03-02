from data_base.configSQL import *
from schems.users import *

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter(prefix='/users', tags=['Пользователи'])


@router.get('/', response_model=List[UserOut], summary='Пользователи:')
def list_users(skip: int = 0, limit: int = 20, DataBase: Session = Depends(get_db)):
    return DataBase.query(UserModel).offset(skip).limit(limit).all()


@router.get('/{user_id}', response_model=UserOut, summary='Получить пользователя:')
def get_user(user_id: int, DataBase: Session = Depends(get_db)):
    user = DataBase.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail='Пользователя не существует.')
    return user


@router.post('/', response_model=UserOut, status_code=status.HTTP_201_CREATED,
             summary='Создать пользователя:')
def create_user(payload: UserCreate, DataBase: Session = Depends(get_db)):
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


@router.put('/{user_id}', response_model=UserOut, summary='Редактировать профиль:')
def update_user(user_id: int, payload: UserUpdate,
                DataBase: Session = Depends(get_db)):
    user = DataBase.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail='Пользователь не существует.')
    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)
    DataBase.commit()
    DataBase.refresh(user)
    return user


@router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT,
               summary='Удалить аккаунт:')
def delete_user(user_id: int, DataBase: Session = Depends(get_db)):
    user = DataBase.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail='Пользователь не существует.')
    DataBase.delete(user)
    DataBase.commit()
