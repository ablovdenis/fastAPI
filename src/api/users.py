from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..domain.users.use_cases.crud_users import MethodsForUser


from ..infrastructure.sqlite.database import get_db
from ..infrastructure.sqlite.models.user_models import UserModel
from ..schems.users import UserCreate, UserOut, UserUpdate

router = APIRouter(prefix='/users', tags=['Пользователи'])


@router.get('/', response_model=List[UserOut], summary='Пользователи:')
def list_users(skip: int = 0, limit: int = 20, DataBase: Session = Depends(get_db)) -> List[UserOut]:
    use_case = MethodsForUser()
    return use_case.get(DataBase, skip, limit)


@router.get('/{nickname}', response_model=UserOut, summary='Получить пользователя:')
def get_user(nickname: str, DataBase: Session = Depends(get_db)) -> UserOut:
    use_case = MethodsForUser()
    return use_case.get_detail(DataBase, nickname)


@router.post('/', response_model=UserOut, status_code=status.HTTP_201_CREATED,
             summary='Создать пользователя:')
def create_user(payload: UserCreate, DataBase: Session = Depends(get_db)) -> UserOut:
    use_case = MethodsForUser()
    return use_case.create(DataBase, payload)


@router.put('/{nickname}', response_model=UserOut, summary='Редактировать профиль:')
def update_user(nickname: str, payload: UserUpdate,
                DataBase: Session = Depends(get_db)) -> UserOut:
    use_case = MethodsForUser()
    return use_case.update(DataBase, nickname, payload)


@router.delete('/{nickname}', status_code=status.HTTP_204_NO_CONTENT,
               summary='Удалить аккаунт:')
def delete_user(nickname: str, DataBase: Session = Depends(get_db)):
    use_case = MethodsForUser()
    use_case.destroy(DataBase, nickname)
