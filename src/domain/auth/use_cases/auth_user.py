# WrongUserPasswordException
from sqlalchemy.orm import Session

from src.infrastructure.sqlite.database import get_db
from src.infrastructure.sqlite.repositories.users import UserRepository
from src.schems.users import UserOut
from src.resources.auth import verify_password
from src.core.exceptions.database_exceptions import UserNotFoundException
from src.core.exceptions.domain_exceptions import UserNotFoundByNicknameException, WrongUserPasswordException


class AuthenticateUserUseCase:
    def __init__(self) -> None:
        self._repo = UserRepository()

    def get_detail(self, DataBase: Session, nickname: str, password: str,
    ) -> UserOut:
        try:
            user_model = self._repo.get_detail(DataBase, nickname)
        except UserNotFoundException:
            raise UserNotFoundByNicknameException(nickname)

        if not verify_password(password, user_model.password):
            raise WrongUserPasswordException()

        return UserOut.model_validate(user_model)