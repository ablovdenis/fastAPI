from typing import List

from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.category_models import CategoryModel
from ..models.location_models import LocationModel
from ..models.post_models import PostModel
from ..models.user_models import UserModel
from ....schems.posts import PostCreateAndUpdate

from src.core.exceptions.database_exceptions import (CredentialException, UserNotFoundException,
                                                     CategoryNotFoundException,
                                                     LocationNotFoundException, 
                                                     PostNotFoundException)

class PostRepository:
    def __init__(self):
        pass

    async def get(self, DataBase: AsyncSession,
            skip: int,
            limit: int,
            published_only: bool) -> List[PostModel]:
        stmt = select(PostModel)
        if published_only:
            stmt = stmt.where(PostModel.is_published.is_(True))
        stmt = stmt.order_by(PostModel.pub_date.desc()).offset(skip).limit(limit)
        result = await DataBase.execute(stmt)
        return result.scalars().all()

    async def get_detail(self, DataBase: AsyncSession, post_id: int) -> PostModel:
        stmt = (
            select(PostModel)
            .where(PostModel.id == post_id)
            .options(
                selectinload(PostModel.author),
                selectinload(PostModel.category),
                selectinload(PostModel.location),
                selectinload(PostModel.comments),
            )
        )
        result = await DataBase.execute(stmt)
        post = result.unique().scalar_one_or_none()
        if not post:
            raise PostNotFoundException()
        return post

    async def create(self, DataBase: AsyncSession, payload: PostCreateAndUpdate,
               nickname: str) -> PostModel:
        stmt_user = select(UserModel).where(UserModel.nickname == nickname)
        user_result = await DataBase.execute(stmt_user)
        author = user_result.scalar_one_or_none()
        if not author:
            raise UserNotFoundException()

        stmt_cat = select(CategoryModel).where(CategoryModel.slug == payload.category_slug)
        cat_result = await DataBase.execute(stmt_cat)
        category = cat_result.scalar_one_or_none()
        if not category:
            raise CategoryNotFoundException()

        stmt_loc = select(LocationModel).where(LocationModel.name == payload.location_name)
        loc_result = await DataBase.execute(stmt_loc)
        location = loc_result.scalar_one_or_none()
        if not location:
            raise LocationNotFoundException()

        dict_ = payload.model_dump(exclude={'location_name', 'author_nickname', 'category_slug'})
        dict_.update(
            location_id=location.id,
            category_id=category.id,
            author_id=author.id,
        )
        post = PostModel(**dict_)
        DataBase.add(post)
        await DataBase.commit()
        await DataBase.refresh(post)
        return post

    async def update_without_image(self, DataBase: AsyncSession, payload: PostCreateAndUpdate,
               post_id: int, nickname: str) -> PostModel:
        stmt_post = select(PostModel).where(PostModel.id == post_id)
        post_result = await DataBase.execute(stmt_post)
        post = post_result.scalar_one_or_none()
        if not post:
            raise PostNotFoundException()

        stmt_user = select(UserModel).where(UserModel.nickname == nickname)
        user_result = await DataBase.execute(stmt_user)
        user = user_result.scalar_one_or_none()
        if not user or post.author_id != user.id:
            raise CredentialException()

        update_data = payload.model_dump(exclude_unset=True)
        if 'category_slug' in update_data:
            stmt_cat = select(CategoryModel).where(CategoryModel.slug == payload.category_slug)
            cat_result = await DataBase.execute(stmt_cat)
            category = cat_result.scalar_one_or_none()
            if not category:
                raise CategoryNotFoundException()
            update_data['category_id'] = category.id
            del update_data['category_slug']

        if 'location_name' in update_data:
            stmt_loc = select(LocationModel).where(LocationModel.name == payload.location_name)
            loc_result = await DataBase.execute(stmt_loc)
            location = loc_result.scalar_one_or_none()
            if not location:
                raise LocationNotFoundException()
            update_data['location_id'] = location.id
            del update_data['location_name']

        update_data.pop('author_nickname', None)

        for field, value in update_data.items():
            setattr(post, field, value)

        await DataBase.commit()
        await DataBase.refresh(post)
        return post

    async def update_image(self, DataBase: AsyncSession, image: str,
               post_id: int, nickname: int) -> PostModel:
        stmt_post = select(PostModel).where(PostModel.id == post_id)
        post_result = await DataBase.execute(stmt_post)
        post = post_result.scalar_one_or_none()
        if not post:
            raise PostNotFoundException()

        stmt_user = select(UserModel).where(UserModel.nickname == nickname)
        user_result = await DataBase.execute(stmt_user)
        user = user_result.scalar_one_or_none()
        if not user or post.author_id != user.id:
            raise CredentialException()

        post.image = image
        await DataBase.commit()
        await DataBase.refresh(post)
        return post

    async def destroy(self, DataBase: AsyncSession, post_id: int, nickname: str):
        post = await self.get_detail(DataBase, post_id)
        stmt_user = select(UserModel).where(UserModel.nickname == nickname)
        user_result = await DataBase.execute(stmt_user)
        user = user_result.scalar_one_or_none()
        if not user or post.author_id != user.id:
            raise CredentialException()

        await DataBase.delete(post)
        await DataBase.commit()