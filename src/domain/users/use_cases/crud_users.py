from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from src.resources.auth import get_password_hash
from src.core.exceptions.domain_exceptions import (UserNicknameIsNotUniqueException,
                                                   UserNotFoundByNicknameException,
                                                   UserEmailIsNotUniqueException)
from src.core.exceptions.database_exceptions import (UserNotFoundException,
                                                     UserByNicknameAlreadyExistsException,
                                                     UserByEmailAlreadyExistsException)

from ....infrastructure.postgre.repositories.users import UserRepository
from ....schems.users import UserCreate, UserOut, UserUpdate


class MethodsForUser:
    def __init__(self):
        self._repo = UserRepository()

    async def get(self, DataBase: AsyncSession, skip: int, limit: int) -> List[UserOut]:
        return [UserOut.model_validate(user) for user in await self._repo.get(DataBase, skip, limit)]

    async def get_detail(self, DataBase: AsyncSession, nickname: str) -> UserOut:
        try:
            user_model = await self._repo.get_detail(DataBase, nickname)
        except UserNotFoundException:
            raise UserNotFoundByNicknameException(nickname)
        return UserOut.model_validate(user_model)

    async def create(self, DataBase: AsyncSession, payload: UserCreate) -> UserOut:
        payload.password = get_password_hash(payload.password)
        try:
            user_model = await self._repo.create(DataBase, payload)
        except UserByNicknameAlreadyExistsException:
            raise UserNicknameIsNotUniqueException(payload.nickname)
        except UserByEmailAlreadyExistsException:
            raise UserEmailIsNotUniqueException(payload.email)
        return UserOut.model_validate(user_model)

    async def update(self, DataBase: AsyncSession, nickname: str, payload: UserUpdate) -> UserOut:
        try:
            user_model = await self._repo.update(DataBase, nickname, payload)
        except UserNotFoundException:
            raise UserNotFoundByNicknameException(nickname)
        except UserByEmailAlreadyExistsException:
            raise UserEmailIsNotUniqueException(payload.email)
        return UserOut.model_validate(user_model)
    
    async def destroy(self, DataBase: AsyncSession, nickname: str) -> UserOut:
        try:
            await self._repo.destroy(DataBase, nickname)
        except UserNotFoundException:
            raise UserNotFoundByNicknameException(nickname)
