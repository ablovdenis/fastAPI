from typing import List

from sqlalchemy.orm import Session

from ....infrastructure.sqlite.repositories.posts import PostRepository
from ....schems.posts import PostCreate, PostDetail, PostOut, PostUpdate

from src.core.exceptions.database_exceptions import (UserNotFoundException,
                                                     CategoryNotFoundException,
                                                     LocationNotFoundException, 
                                                     PostNotFoundException)
from src.core.exceptions.domain_exceptions import (PostNotFoundByIDException,
                                                   PostDontCreateException,
                                                   PostDontChangeException)


class MethodsForPost:
    def __init__(self):
        self._repo = PostRepository()

    def get(self, DataBase: Session, skip: int, limit: int, published_only: bool) -> List[PostOut]:
        return [PostOut.model_validate(user) for user in self._repo.get(DataBase, skip, limit, published_only)]

    def get_detail(self, DataBase: Session, post_id: int) -> PostDetail:
        try:
            post_model = self._repo.get_detail(DataBase, post_id)
        except PostNotFoundException:
            raise PostNotFoundByIDException(post_id)
        return PostDetail.model_validate(post_model)

    def create(self, DataBase: Session, payload: PostCreate) -> PostOut:
        try:
            post_model = self._repo.create(DataBase, payload)
        except UserNotFoundException:
            raise PostDontCreateException('автор не найден')
        except CategoryNotFoundException:
            raise PostDontCreateException('категория не найдена')
        except LocationNotFoundException:
            raise PostDontCreateException('локация не найдена')
        return PostOut.model_validate(post_model)

    def update(self, DataBase: Session, post_id: int, payload: PostUpdate) -> PostOut:
        try:
            post_model = self._repo.update(DataBase, post_id, payload)
        except PostNotFoundException:
            raise PostNotFoundByIDException(post_id)
        except CategoryNotFoundException:
            raise PostDontChangeException('категория не найдена')
        except LocationNotFoundException:
            raise PostDontChangeException('локация не найдена')
        return PostOut.model_validate(post_model)
    
    def destroy(self, DataBase: Session, post_id: int):
        try:
            self._repo.destroy(DataBase, post_id)
        except PostNotFoundException:
            raise PostNotFoundByIDException(post_id)