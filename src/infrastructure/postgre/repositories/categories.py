from typing import List

from sqlalchemy import select, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.category_models import CategoryModel
from ....schems.categories import CategoryUpdateAndCreate

from src.core.exceptions.database_exceptions import CategoryNotFoundException, CategoryAlreadyExistsException

class CategoryRepository:
    def __init__(self):
        pass

    async def get(self, DataBase: AsyncSession, skip: int, limit: int) -> List[CategoryModel]:
        stmt = select(CategoryModel).offset(skip).limit(limit)
        result = await DataBase.execute(stmt)
        return result.scalars().all()

    async def get_detail(self, DataBase: AsyncSession, category_slug: str) -> CategoryModel:
        stmt = select(CategoryModel).where(CategoryModel.slug == category_slug)
        result = await DataBase.execute(stmt)
        category = result.scalar_one_or_none()
        if not category:
            raise CategoryNotFoundException()
        return category

    async def create(self, DataBase: AsyncSession, payload: CategoryUpdateAndCreate) -> CategoryModel:
        category = CategoryModel(**payload.model_dump())
        DataBase.add(category)
        try:
            await DataBase.commit()
        except IntegrityError:
            raise CategoryAlreadyExistsException()
        await DataBase.refresh(category)
        return category

    async def update(self, DataBase: AsyncSession, category_slug: str, payload: CategoryUpdateAndCreate) -> CategoryModel:
        category = await self.get_detail(DataBase, category_slug)
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(category, field, value)
        try:
            await DataBase.commit()
        except IntegrityError:
            raise CategoryAlreadyExistsException()
        await DataBase.refresh(category)
        return category

    async def destroy(self, DataBase: AsyncSession, category_slug: str):
        stmt = delete(CategoryModel).where(CategoryModel.slug == category_slug)
        result = await DataBase.execute(stmt)
        await DataBase.commit()
        if result.rowcount == 0:
            raise CategoryNotFoundException()