from typing import List

from sqlalchemy.orm import Session

from ....infrastructure.sqlite.repositories.posts import PostRepository
from ....schems.posts import PostCreateAndUpdate, PostDetail, PostOut

from src.core.exceptions.database_exceptions import (CredentialException, UserNotFoundException,
                                                     CategoryNotFoundException,
                                                     LocationNotFoundException, 
                                                     PostNotFoundException)
from src.core.exceptions.domain_exceptions import (PostDontDestroyException, PostNotFoundByIDException,
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

    def create(self, DataBase: Session, payload: PostCreateAndUpdate,
               nickname: str) -> PostOut:
        try:
            post_model = self._repo.create(DataBase, payload, nickname)
        except UserNotFoundException:
            raise PostDontCreateException('автор не найден')
        except CategoryNotFoundException:
            raise PostDontCreateException('категория не найдена')
        except LocationNotFoundException:
            raise PostDontCreateException('локация не найдена')
        return PostOut.model_validate(post_model)

    def update(self, DataBase: Session, payload: PostCreateAndUpdate,
               post_id: int, author_id: int) -> PostOut:
        try:
            post_model = self._repo.update(DataBase, payload, post_id, author_id)
        except PostNotFoundException:
            raise PostNotFoundByIDException(post_id)
        except CategoryNotFoundException:
            raise PostDontChangeException('категория не найдена')
        except LocationNotFoundException:
            raise PostDontChangeException('локация не найдена')
        except CredentialException:
            raise PostDontChangeException('данный пост не принадлежит этому пользователю')
        return PostOut.model_validate(post_model)
    
    def destroy(self, DataBase: Session, post_id: int, author_id: int):
        try:
            self._repo.destroy(DataBase, post_id, author_id)
        except PostNotFoundException:
            raise PostNotFoundByIDException(post_id)
        except CredentialException:
            raise PostDontDestroyException('данный пост не принадлежит этому пользователю')