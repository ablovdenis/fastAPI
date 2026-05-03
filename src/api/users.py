import logging

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.services.auth import get_current_user

from ..domain.users.use_cases.crud_users import MethodsForUser

from src.core.exceptions.domain_exceptions import (UserNicknameIsNotUniqueException,
                                                   UserNotFoundByNicknameException,
                                                   UserEmailIsNotUniqueException)

from ..infrastructure.postgre.database import get_db
from ..schems.users import UserCreate, UserOut, UserUpdate

logger = logging.getLogger(__name__)

router = APIRouter(prefix='/users', tags=['Пользователи'])


@router.get('/all', response_model=List[UserOut], summary='Пользователи:')
def list_users(skip: int = 0, limit: int = 20, DataBase: Session = Depends(get_db),
               _: UserOut = Depends(get_current_user)) -> List[UserOut]:
    logger.info(f"Запрос списка пользователей: skip={skip}, limit={limit}")
    use_case = MethodsForUser()
    result = use_case.get(DataBase, skip, limit)
    logger.info(f"Возвращено {len(result)} пользователей")
    return result


@router.get('/{nickname}', response_model=UserOut, summary='Получить любого пользователя по никнейму:')
def get_user(nickname: str, DataBase: Session = Depends(get_db),
             _: UserOut = Depends(get_current_user)) -> UserOut:
    logger.info(f"Запрос пользователя по никнейму='{nickname}'")
    use_case = MethodsForUser()
    try:
        result = use_case.get_detail(DataBase, nickname)
        logger.info(f"Пользователь '{nickname}' найден")
        return result
    except UserNotFoundByNicknameException as e:
        logger.warning(f"Пользователь '{nickname}' не найден")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail())


@router.get('/', response_model=UserOut, summary='Получить данные о себе:')
def get_user(user: UserOut = Depends(get_current_user)) -> UserOut:
    logger.info(f"Запрос данных текущего пользователя: {user.nickname}")
    return user


@router.post('/', response_model=UserOut, status_code=status.HTTP_201_CREATED,
             summary='Создать пользователя:')
def create_user(payload: UserCreate, DataBase: Session = Depends(get_db)) -> UserOut:
    logger.info(f"Попытка создания пользователя с никнеймом '{payload.nickname}'")
    use_case = MethodsForUser()
    try:
        result = use_case.create(DataBase, payload)
        logger.info(f"Создан пользователь: id={result.id}, nickname='{result.nickname}'")
        return result
    except UserNicknameIsNotUniqueException as e:
        logger.warning(f"Ошибка создания: никнейм '{payload.nickname}' уже существует")
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=e.get_detail())
    except UserEmailIsNotUniqueException as e:
        logger.warning(f"Ошибка создания: email '{payload.email}' уже существует")
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=e.get_detail())


@router.put('/', response_model=UserOut, summary='Редактировать профиль:')
def update_user(payload: UserUpdate, DataBase: Session = Depends(get_db),
                user: UserOut = Depends(get_current_user)) -> UserOut:
    logger.info(f"Попытка обновления профиля пользователя {user.nickname}")
    use_case = MethodsForUser()
    try:
        result = use_case.update(DataBase, user.nickname, payload)
        logger.info(f"Профиль пользователя {user.nickname} обновлён")
        return result
    except UserNotFoundByNicknameException as e:
        logger.warning(f"Пользователь {user.nickname} не найден при обновлении")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail())
    except UserEmailIsNotUniqueException as e:
        logger.warning(f"Ошибка обновления: email '{payload.email}' уже используется")
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=e.get_detail())


@router.delete('/', status_code=status.HTTP_204_NO_CONTENT,
               summary='Удалить аккаунт:')
def delete_user(DataBase: Session = Depends(get_db), user: UserOut = Depends(get_current_user)):
    logger.info(f"Попытка удаления аккаунта пользователя {user.nickname}")
    use_case = MethodsForUser()
    try:
        use_case.destroy(DataBase, user.nickname)
        logger.info(f"Аккаунт пользователя {user.nickname} удалён")
    except UserNotFoundByNicknameException as e:
        logger.warning(f"Пользователь {user.nickname} не найден при удалении")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail())