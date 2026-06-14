import logging

from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions.auth_exceptions import CredentialsException
from src.core.exceptions.database_exceptions import UserNotFoundException
from src.domain.auth.use_cases.create_refresh_token import CreateRefreshTokenUseCase
from src.infrastructure.postgre.repositories.users import UserRepository
from src.infrastructure.postgre.database import get_db
from src.schems.auth import Token
from src.domain.auth.use_cases.auth_user import AuthenticateUserUseCase
from src.domain.auth.use_cases.create_access_token import CreateAccessTokenUseCase
from src.core.exceptions.domain_exceptions import WrongUserPasswordException, UserNotFoundByNicknameException
from src.api.depends import create_access_token_use_case, auth_user_use_case, create_refresh_token_use_case
from src.core.config import settings

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_use_case: AuthenticateUserUseCase = Depends(auth_user_use_case),
    DataBase: AsyncSession = Depends(get_db)
) -> Token:
    logger.info(f"Попытка входа в систему: username={form_data.username}")
    try:
        user = await auth_use_case.get_detail(DataBase, form_data.username, form_data.password)
        logger.info(f"Пользователь {form_data.username} успешно аутентифицирован")
    except WrongUserPasswordException as exc:
        logger.warning(f"Неудачная попытка входа: username={form_data.username} - неверный пароль")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=exc.get_detail(),
            headers={"WWW-Authenticate": "Bearer"},
        )
    except UserNotFoundByNicknameException as exc:
        logger.warning(f"Неудачная попытка входа: username={form_data.username} - пользователь не найден")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail())

    access_token = await create_access_token_use_case().create_token(user.nickname)
    refresh_token = await create_refresh_token_use_case().create_token(user.nickname)
    logger.info(f"Для пользователя {form_data.username} выдан JWT токен (токен не логируется)")
    return Token(access_token=access_token,
                 token_type="bearer",
                 refresh_token=refresh_token)


@router.post("/refresh", response_model=Token)
async def refresh_token(
    refresh_token: str,
    DataBase: AsyncSession = Depends(get_db)
) -> Token:
    logger.info(f"Ввод рефреш-токена.")
    payload = jwt.decode(
        token=refresh_token,
        key=settings.SECRET_AUTH_KEY.get_secret_value(),
        algorithms=[settings.AUTH_ALGORITHM],
    )
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Некорректный рефреш-токен."
        )
    nickname = payload.get("sub")
    if not nickname:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Некорректный рефреш-токен."
        )
    try:
        user = await UserRepository().get_detail(DataBase, nickname)
    except UserNotFoundException:
        raise CredentialsException(detail="Данные авторизации не получилось проверить.")

    new_access_token = await create_access_token_use_case().create_token(user.nickname)
    logger.info(f"Для пользователя {nickname} выдан JWT токен по рефреш-токену.")
    return Token(access_token=new_access_token,
                 token_type="bearer",
                 refresh_token=refresh_token)
