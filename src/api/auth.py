import logging

from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.infrastructure.postgre.database import get_db
from src.schems.auth import Token
from src.domain.auth.use_cases.auth_user import AuthenticateUserUseCase
from src.domain.auth.use_cases.create_access_token import CreateAccessTokenUseCase
from src.core.exceptions.domain_exceptions import WrongUserPasswordException, UserNotFoundByNicknameException
from src.api.depends import create_access_token_use_case, auth_user_use_case

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/token", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_use_case: AuthenticateUserUseCase = Depends(auth_user_use_case),
    create_token_use_case: CreateAccessTokenUseCase = Depends(create_access_token_use_case),
    DataBase: Session = Depends(get_db)
) -> Token:
    logger.info(f"Попытка входа в систему: username={form_data.username}")
    try:
        user = auth_use_case.get_detail(DataBase, form_data.username, form_data.password)
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

    access_token = create_token_use_case.create_token(user.nickname)
    logger.info(f"Для пользователя {form_data.username} выдан JWT токен (токен не логируется)")
    return Token(access_token=access_token, token_type="bearer")