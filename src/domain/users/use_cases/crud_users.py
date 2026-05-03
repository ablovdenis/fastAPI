from typing import List

from sqlalchemy.orm import Session

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

    def get(self, DataBase: Session, skip: int, limit: int) -> List[UserOut]:
        return [UserOut.model_validate(user) for user in self._repo.get(DataBase, skip, limit)]

    def get_detail(self, DataBase: Session, nickname: str) -> UserOut:
        try:
            user_model = self._repo.get_detail(DataBase, nickname)
        except UserNotFoundException:
            raise UserNotFoundByNicknameException(nickname)
        return UserOut.model_validate(user_model)

    def create(self, DataBase: Session, payload: UserCreate) -> UserOut:
        payload.password = get_password_hash(payload.password)
        try:
            user_model = self._repo.create(DataBase, payload)
        except UserByNicknameAlreadyExistsException:
            raise UserNicknameIsNotUniqueException(payload.nickname)
        except UserByEmailAlreadyExistsException:
            raise UserEmailIsNotUniqueException(payload.email)
        return UserOut.model_validate(user_model)

    def update(self, DataBase: Session, nickname: str, payload: UserUpdate) -> UserOut:
        try:
            user_model = self._repo.update(DataBase, nickname, payload)
        except UserNotFoundException:
            raise UserNotFoundByNicknameException(nickname)
        except UserByEmailAlreadyExistsException:
            raise UserEmailIsNotUniqueException(payload.email)
        return UserOut.model_validate(user_model)
    
    def destroy(self, DataBase: Session, nickname: str) -> UserOut:
        try:
            self._repo.destroy(DataBase, nickname)
        except UserNotFoundException:
            raise UserNotFoundByNicknameException(nickname)
