from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.comment_models import CommentModel
from ..models.post_models import PostModel
from ....schems.comments import CommentCreate, CommentUpdate

from src.core.exceptions.database_exceptions import (CredentialException, PostNotFoundException,
                                                     CommentNotFoundException)

class CommentRepository:
    def __init__(self):
        pass

    async def get(self, DataBase: AsyncSession, post_id: int | None, skip: int, limit: int) -> List[CommentModel]:
        if post_id is not None:
            stmt_post = select(PostModel).where(PostModel.id == post_id)
            post = (await DataBase.execute(stmt_post)).scalar_one_or_none()
            if not post:
                raise PostNotFoundException()
        stmt = select(CommentModel).order_by(CommentModel.created_at).offset(skip).limit(limit)
        if post_id is not None:
            stmt = stmt.where(CommentModel.post_id == post_id)
        result = await DataBase.execute(stmt)
        return result.scalars().all()

    async def get_detail(self, DataBase: AsyncSession, comment_id: int) -> CommentModel:
        stmt = select(CommentModel).where(CommentModel.id == comment_id)
        result = await DataBase.execute(stmt)
        comment = result.scalar_one_or_none()
        if not comment:
            raise CommentNotFoundException()
        return comment

    async def create(self, DataBase: AsyncSession, payload: CommentCreate, author_id: int) -> CommentModel:
        stmt_post = select(PostModel).where(PostModel.id == payload.post_id)
        post = (await DataBase.execute(stmt_post)).scalar_one_or_none()
        if not post:
            raise PostNotFoundException()
        dict_ = payload.model_dump() | {'author_id': author_id}
        comment = CommentModel(**dict_)
        DataBase.add(comment)
        await DataBase.commit()
        await DataBase.refresh(comment)
        return comment


    async def update(self, DataBase: AsyncSession, comment_id: int, payload: CommentUpdate, author_id: str) -> CommentModel:
        comment = await self.get_detail(DataBase, comment_id)
        if comment.author_id != author_id:
            raise CredentialException()
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(comment, field, value)
        await DataBase.commit()
        await DataBase.refresh(comment)
        return comment

    async def destroy(self, DataBase: AsyncSession, comment_id: int, author_id: str):
        comment = await self.get_detail(DataBase, comment_id)
        if comment.author_id != author_id:
            raise CredentialException()
        await DataBase.delete(comment)
        await DataBase.commit()