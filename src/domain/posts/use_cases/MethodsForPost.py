from typing import List

from sqlalchemy.orm import Session

from ....infrastructure.sqlite.repositories.posts import PostRepository
from ....schems.posts import PostCreate, PostDetail, PostOut, PostUpdate



class MethodsForPost:
    def __init__(self):
        self._repo = PostRepository()

    def get(self, DataBase: Session, skip: int, limit: int, published_only: bool) -> List[PostOut]:
        return [PostOut.model_validate(user) for user in self._repo.get(DataBase, skip, limit, published_only)]

    def get_detail(self, DataBase: Session, post_id: int) -> PostDetail:
        return PostDetail.model_validate(self._repo.get_detail(DataBase, post_id))

    def create(self, DataBase: Session, payload: PostCreate) -> PostOut:
        return PostOut.model_validate(self._repo.create(DataBase, payload))

    def update(self, DataBase: Session, post_id: int, payload: PostUpdate) -> PostOut:
        return PostOut.model_validate(self._repo.update(DataBase, post_id, payload))
    
    def destroy(self, DataBase: Session, post_id: int):
        self._repo.destroy(DataBase, post_id)