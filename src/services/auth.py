from fastapi import Depends
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from src.core.exceptions.database_exceptions import UserNotFoundException
from src.core.exceptions.auth_exceptions import CredentialsException
from src.core.config import settings

from src.schems.users import UserOut

from src.infrastructure.sqlite.database import get_db
from src.infrastructure.sqlite.repositories.users import UserRepository

from src.resources.auth import oauth2_scheme


def get_current_user(token: str = Depends(oauth2_scheme)) -> UserOut:
    AUTH_MESSAGE_EXCEPTION = "Данные авторизации не получилось проверить."
    repo: UserRepository = UserRepository()

    try:
        payload = jwt.decode(
            token=token,
            key=settings.SECRET_AUTH_KEY.get_secret_value(),
            algorithms=[settings.AUTH_ALGORITHM],
        )
        nickname: str = payload.get("sub") # payload - это словарь, у которого есть ключ "sub",
                                           # хранящий субъект, которому выдан токен.
        if nickname is None:
            raise CredentialsException(detail=AUTH_MESSAGE_EXCEPTION)
    except JWTError:
        raise CredentialsException(detail=AUTH_MESSAGE_EXCEPTION)

    try:
        db: Session = next(get_db())
        user = repo.get_detail(db, nickname)
    except UserNotFoundException:
        raise CredentialsException(detail=AUTH_MESSAGE_EXCEPTION)

    return UserOut.model_validate(obj=user)