from typing import List

from sqlalchemy.orm import Session

from ....infrastructure.sqlite.repositories.comments import CommentRepository
from ....schems.comments import CommentCreate, CommentOut, CommentUpdate



class MethodsForComment:
    def __init__(self):
        self._repo = CommentRepository()

    def get(self, DataBase: Session, post_id: int | None, skip: int, limit: int) -> List[CommentOut]:
        return [CommentOut.model_validate(user) for user in self._repo.get(DataBase, post_id, skip, limit)]

    def get_detail(self, DataBase: Session, comment_id: int) -> CommentOut:
        return CommentOut.model_validate(self._repo.get_detail(DataBase, comment_id))

    def create(self, DataBase: Session, payload: CommentCreate) -> CommentOut:
        return CommentOut.model_validate(self._repo.create(DataBase, payload))

    def update(self, DataBase: Session, comment_id: int, payload: CommentUpdate) -> CommentOut:
        return CommentOut.model_validate(self._repo.update(DataBase, comment_id, payload))
    
    def destroy(self, DataBase: Session, comment_id: int):
        self._repo.destroy(DataBase, comment_id)