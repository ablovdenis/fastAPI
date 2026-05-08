from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from ....infrastructure.postgre.repositories.categories import CategoryRepository
from ....schems.categories import CategoryOut, CategoryUpdateAndCreate

from src.core.exceptions.domain_exceptions import CategoryNotFoundBySlugException, CategoryIsNotUniqueException
from src.core.exceptions.database_exceptions import CategoryNotFoundException, CategoryAlreadyExistsException


class MethodsForCategory:
    def __init__(self):
        self._repo = CategoryRepository()

    async def get(self, DataBase: AsyncSession, skip: int, limit: int) -> List[CategoryOut]:
        return [CategoryOut.model_validate(category) for category in await self._repo.get(DataBase, skip, limit)]

    async def get_detail(self, DataBase: AsyncSession, category_slug: str) -> CategoryOut:
        try:
            category_model = await self._repo.get_detail(DataBase, category_slug)
        except CategoryNotFoundException:
            raise CategoryNotFoundBySlugException(category_slug)
        return CategoryOut.model_validate(category_model)

    async def create(self, DataBase: AsyncSession, payload: CategoryUpdateAndCreate) -> CategoryOut:
        try:
            category_model = await self._repo.create(DataBase, payload)
        except CategoryAlreadyExistsException:
            raise CategoryIsNotUniqueException(payload.slug)
        return CategoryOut.model_validate(category_model)

    async def update(self, DataBase: AsyncSession, category_slug: str, payload: CategoryUpdateAndCreate) -> CategoryOut:
        try:
            category_model = await self._repo.update(DataBase, category_slug, payload)
        except CategoryNotFoundException:
            raise CategoryNotFoundBySlugException(category_slug)
        except CategoryAlreadyExistsException:
            raise CategoryIsNotUniqueException(payload.slug)
        return CategoryOut.model_validate(category_model)
    
    async def destroy(self, DataBase: AsyncSession, category_slug: str):
        try:
            await self._repo.destroy(DataBase, category_slug)
        except CategoryNotFoundException:
            raise CategoryNotFoundBySlugException(category_slug)
