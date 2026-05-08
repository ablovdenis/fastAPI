from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from ....infrastructure.postgre.repositories.comments import CommentRepository
from ....schems.comments import CommentCreate, CommentOut, CommentUpdate

from src.core.exceptions.database_exceptions import (CredentialException, UserNotFoundException,
                                                     PostNotFoundException,
                                                     CommentNotFoundException)
from src.core.exceptions.domain_exceptions import (CommentDontChangeException, CommentDontDestroyException, CommentNotFoundByIDException,
                                                   CommentDontCreateException,
                                                   PostNotFoundByIDException)


class MethodsForComment:
    def __init__(self):
        self._repo = CommentRepository()

    async def get(self, DataBase: AsyncSession, post_id: int | None, skip: int, limit: int) -> List[CommentOut]:
        try:
            return [CommentOut.model_validate(user) for user in await self._repo.get(DataBase, post_id, skip, limit)]
        except PostNotFoundException:
            raise PostNotFoundByIDException(post_id)

    async def get_detail(self, DataBase: AsyncSession, comment_id: int) -> CommentOut:
        try:
            comment_model = await self._repo.get_detail(DataBase, comment_id)
        except CommentNotFoundException:
            raise CommentNotFoundByIDException(comment_id)
        return CommentOut.model_validate(comment_model)

    async def create(self, DataBase: AsyncSession, payload: CommentCreate, author_id: int) -> CommentOut:
        try:
            comment_model = await self._repo.create(DataBase, payload, author_id)
        except PostNotFoundException:
            raise CommentDontCreateException('пост не найден')
        except UserNotFoundException:
            raise CommentDontCreateException('автор не найден')
        return CommentOut.model_validate(comment_model)

    async def update(self, DataBase: AsyncSession, comment_id: int, payload: CommentUpdate,
               author_id: str) -> CommentOut:
        try:
            comment_model = await self._repo.update(DataBase, comment_id, payload, author_id)
        except CommentNotFoundException:
            raise CommentNotFoundByIDException(comment_id)
        except CredentialException:
            raise CommentDontChangeException('данный пост не принадлежит этому пользователю')
        return CommentOut.model_validate(comment_model)
    
    async def destroy(self, DataBase: AsyncSession, comment_id: int, author_id: int):
        try:
            await self._repo.destroy(DataBase, comment_id, author_id)
        except CommentNotFoundException:
            raise CommentNotFoundByIDException(comment_id)
        except CredentialException:
            raise CommentDontDestroyException('данный пост не принадлежит этому пользователю')
