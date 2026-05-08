from typing import List

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.location_models import LocationModel
from ....schems.locations import LocationUpdateAndCreate

from src.core.exceptions.database_exceptions import LocationNotFoundException, LocationAlreadyExistsException

class LocationRepository:
    def __init__(self):
        pass

    async def get(self, DataBase: AsyncSession, skip: int, limit: int) -> List[LocationModel]:
        stmt = select(LocationModel).offset(skip).limit(limit)
        result = await DataBase.execute(stmt)
        return result.scalars().all()

    async def get_detail(self, DataBase: AsyncSession, name: str) -> LocationModel:
        stmt = select(LocationModel).where(LocationModel.name == name)
        result = await DataBase.execute(stmt)
        location = result.scalar_one_or_none()
        if not location:
            raise LocationNotFoundException()
        return location

    async def create(self, DataBase: AsyncSession, payload: LocationUpdateAndCreate) -> LocationModel:
        location = LocationModel(**payload.model_dump())
        DataBase.add(location)
        try:
            await DataBase.commit()
        except IntegrityError:
            raise LocationAlreadyExistsException()
        await DataBase.refresh(location)
        return location

    async def update(self, DataBase: AsyncSession, name: str, payload: LocationUpdateAndCreate) -> LocationModel:
        location = await self.get_detail(DataBase, name)
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(location, field, value)
        try:
            await DataBase.commit()
        except IntegrityError:
            raise LocationAlreadyExistsException()
        await DataBase.refresh(location)
        return location

    async def destroy(self, DataBase: AsyncSession, name: str):
        location = await self.get_detail(DataBase, name)
        await DataBase.delete(location)
        await DataBase.commit()