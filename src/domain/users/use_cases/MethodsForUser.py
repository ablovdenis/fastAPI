from typing import List

from sqlalchemy.orm import Session

from ....infrastructure.sqlite.repositories.users import UserRepository
from ....schems.users import UserCreate, UserOut, UserUpdate


class MethodsForUser:
    def __init__(self):
        self._repo = UserRepository()

    def get(self, DataBase: Session, skip: int, limit: int) -> List[UserOut]:
        return [UserOut.model_validate(user) for user in self._repo.get(DataBase, skip, limit)]

    def get_detail(self, DataBase: Session, user_id: int) -> UserOut:
        return UserOut.model_validate(self._repo.get_detail(DataBase, user_id))

    def create(self, DataBase: Session, payload: UserCreate) -> UserOut:
        return UserOut.model_validate(self._repo.create(DataBase, payload))

    def update(self, DataBase: Session, user_id: int, payload: UserUpdate) -> UserOut:
        return UserOut.model_validate(self._repo.update(DataBase, user_id, payload))
    
    def destroy(self, DataBase: Session, user_id: int):
        self._repo.destroy(DataBase, user_id)