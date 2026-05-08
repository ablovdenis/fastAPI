# WrongUserPasswordException
import logging

from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.postgre.repositories.users import UserRepository
from src.schems.users import UserOut
from src.resources.auth import verify_password
from src.core.exceptions.database_exceptions import UserNotFoundException
from src.core.exceptions.domain_exceptions import UserNotFoundByNicknameException, WrongUserPasswordException

logger = logging.getLogger(__name__)

class AuthenticateUserUseCase:
    def __init__(self) -> None:
        self._repo = UserRepository()

    async def get_detail(self, DataBase: AsyncSession, nickname: str, password: str,
    ) -> UserOut:
        logger.info(f"Попытка аутентификации пользователя: {nickname}")
        try:
            user_model = await self._repo.get_detail(DataBase, nickname)
            logger.debug(f"Пользователь {nickname} найден в БД")
        except UserNotFoundException:
            logger.warning(f"Пользователь {nickname} не найден")
            raise UserNotFoundByNicknameException(nickname)

        if not verify_password(password, user_model.password):
            logger.warning(f"Неверный пароль для пользователя {nickname}")
            raise WrongUserPasswordException()

        logger.info(f"Пользователь {nickname} успешно аутентифицирован")
        return UserOut.model_validate(user_model)