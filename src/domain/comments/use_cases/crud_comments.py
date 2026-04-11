from typing import List

from sqlalchemy.orm import Session

from ....infrastructure.sqlite.repositories.comments import CommentRepository
from ....schems.comments import CommentCreate, CommentOut, CommentUpdate

from src.core.exceptions.database_exceptions import (UserNotFoundException,
                                                     PostNotFoundException,
                                                     CommentNotFoundException)
from src.core.exceptions.domain_exceptions import (CommentNotFoundByIDException,
                                                   CommentDontCreateException,
                                                   PostNotFoundByIDException)


class MethodsForComment:
    def __init__(self):
        self._repo = CommentRepository()

    def get(self, DataBase: Session, post_id: int | None, skip: int, limit: int) -> List[CommentOut]:
        try:
            return [CommentOut.model_validate(user) for user in self._repo.get(DataBase, post_id, skip, limit)]
        except PostNotFoundException:
            raise PostNotFoundByIDException(post_id)

    def get_detail(self, DataBase: Session, comment_id: int) -> CommentOut:
        try:
            comment_model = self._repo.get_detail(DataBase, comment_id)
        except CommentNotFoundException:
            raise CommentNotFoundByIDException(comment_id)
        return CommentOut.model_validate(comment_model)

    def create(self, DataBase: Session, payload: CommentCreate) -> CommentOut:
        try:
            comment_model = self._repo.create(DataBase, payload)
        except PostNotFoundException:
            raise CommentDontCreateException('пост не найден')
        except UserNotFoundException:
            raise CommentDontCreateException('автор не найден')
        return CommentOut.model_validate(comment_model)

    def update(self, DataBase: Session, comment_id: int, payload: CommentUpdate) -> CommentOut:
        try:
            comment_model = self._repo.update(DataBase, comment_id, payload)
        except CommentNotFoundException:
            raise CommentNotFoundByIDException(comment_id)
        return CommentOut.model_validate(comment_model)
    
    def destroy(self, DataBase: Session, comment_id: int):
        try:
            self._repo.destroy(DataBase, comment_id)
        except CommentNotFoundException:
            raise CommentNotFoundByIDException(comment_id)
