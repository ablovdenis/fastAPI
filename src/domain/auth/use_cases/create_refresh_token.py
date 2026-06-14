import logging
from datetime import datetime, timedelta, timezone

from jose import jwt

from src.core.config import settings

logger = logging.getLogger(__name__)

class CreateRefreshTokenUseCase:
  async def create_token(
            self, nickname: str,
            expires_delta: timedelta | None = None
        ) -> str:
        logger.info(f"Создание рефреш-токена для пользователя: {nickname}")
        logger.debug(
            f"expires_delta: {expires_delta} (если None, используется значение из настроек: {settings.REFRESH_TOKEN_EXPIRE_MINUTES} мин)"
        )
        to_encode = {"sub": nickname}
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
            logger.debug(f"Установлен срок действия рефреш-токена: {expire} (expires_delta={expires_delta})")
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
            logger.debug(f"Установлен срок действия рефреш-токена по умолчанию: {expire}")

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            claims=to_encode,
            key=settings.SECRET_AUTH_KEY.get_secret_value(),
            algorithm=settings.AUTH_ALGORITHM,
        )
        logger.info(f"Рефреш-токен для пользователя {nickname} успешно создан")
        return encoded_jwt