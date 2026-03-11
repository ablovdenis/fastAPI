from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..domain.users.use_cases.MethodsForUser import MethodsForUser


from ..infrastructure.sqlite.configSQL import get_db
from ..infrastructure.sqlite.models.UserModels import UserModel
from ..schems.users import UserCreate, UserOut, UserUpdate

router = APIRouter(prefix='/users', tags=['Пользователи'])


@router.get('/', response_model=List[UserOut], summary='Пользователи:')
def list_users(skip: int = 0, limit: int = 20, DataBase: Session = Depends(get_db)) -> List[UserOut]:
    use_case = MethodsForUser()
    return use_case.get(DataBase, skip, limit)


@router.get('/{user_id}', response_model=UserOut, summary='Получить пользователя:')
def get_user(user_id: int, DataBase: Session = Depends(get_db)) -> UserOut:
    use_case = MethodsForUser()
    return use_case.get_detail(DataBase, user_id)


@router.post('/', response_model=UserOut, status_code=status.HTTP_201_CREATED,
             summary='Создать пользователя:')
def create_user(payload: UserCreate, DataBase: Session = Depends(get_db)) -> UserOut:
    use_case = MethodsForUser()
    return use_case.create(DataBase, payload)


@router.put('/{user_id}', response_model=UserOut, summary='Редактировать профиль:')
def update_user(user_id: int, payload: UserUpdate,
                DataBase: Session = Depends(get_db)) -> UserOut:
    use_case = MethodsForUser()
    return use_case.update(DataBase, user_id, payload)


@router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT,
               summary='Удалить аккаунт:')
def delete_user(user_id: int, DataBase: Session = Depends(get_db)):
    use_case = MethodsForUser()
    use_case.destroy(DataBase, user_id)
