import os
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from ....infrastructure.postgre.repositories.posts import PostRepository
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

    async def get(self, DataBase: AsyncSession, skip: int, limit: int, published_only: bool) -> List[PostOut]:
        return [PostOut.model_validate(user) for user in await self._repo.get(DataBase, skip, limit, published_only)]

    async def get_detail(self, DataBase: AsyncSession, post_id: int) -> PostDetail:
        try:
            post_model = await self._repo.get_detail(DataBase, post_id)
        except PostNotFoundException:
            raise PostNotFoundByIDException(post_id)
        return PostDetail.model_validate(post_model)

    async def create(self, DataBase: AsyncSession, payload: PostCreateAndUpdate,
               nickname: str) -> PostOut:
        try:
            post_model = await self._repo.create(DataBase, payload, nickname)
        except UserNotFoundException:
            raise PostDontCreateException('автор не найден')
        except CategoryNotFoundException:
            raise PostDontCreateException('категория не найдена')
        except LocationNotFoundException:
            raise PostDontCreateException('локация не найдена')
        return PostOut.model_validate(post_model)

    async def update(self, DataBase: AsyncSession, payload: PostCreateAndUpdate,
               post_id: int, nickname: int) -> PostOut:
        try:
            post_model = await self._repo.update_without_image(DataBase, payload, post_id, nickname)
        except PostNotFoundException:
            raise PostNotFoundByIDException(post_id)
        except CategoryNotFoundException:
            raise PostDontChangeException('категория не найдена')
        except LocationNotFoundException:
            raise PostDontChangeException('локация не найдена')
        except CredentialException:
            raise PostDontChangeException('данный пост не принадлежит этому пользователю')
        return PostOut.model_validate(post_model)
    
    async def destroy(self, DataBase: AsyncSession, post_id: int, nickname: str, image_folder="images"):
        try:
            await self._repo.destroy(DataBase, post_id, nickname)
        except PostNotFoundException:
            raise PostNotFoundByIDException(post_id)
        except CredentialException:
            raise PostDontDestroyException('данный пост не принадлежит этому пользователю')