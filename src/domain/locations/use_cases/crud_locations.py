from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from ....infrastructure.postgre.repositories.locations import LocationRepository
from ....schems.locations import LocationOut, LocationUpdateAndCreate

from src.core.exceptions.domain_exceptions import LocationNotFoundByNameException, LocationIsNotUniqueException
from src.core.exceptions.database_exceptions import LocationNotFoundException, LocationAlreadyExistsException


class MethodsForLocation:
    def __init__(self):
        self._repo = LocationRepository()

    async def get(self, DataBase: AsyncSession, skip: int, limit: int) -> List[LocationOut]:
        return [LocationOut.model_validate(location) for location in await self._repo.get(DataBase, skip, limit)]

    async def get_detail(self, DataBase: AsyncSession, name: str) -> LocationOut:
        try:
            location_model = await self._repo.get_detail(DataBase, name)
        except LocationNotFoundException:
            raise LocationNotFoundByNameException(name)
        return LocationOut.model_validate(location_model)

    async def create(self, DataBase: AsyncSession, payload: LocationUpdateAndCreate) -> LocationOut:
        try:
            location_model = await self._repo.create(DataBase, payload)
        except LocationAlreadyExistsException:
            raise LocationIsNotUniqueException(payload.name)
        return LocationOut.model_validate(location_model)

    async def update(self, DataBase: AsyncSession, name: str, payload: LocationUpdateAndCreate) -> LocationOut:
        try:
            location_model = await self._repo.update(DataBase, name, payload)
        except LocationNotFoundException:
            raise LocationNotFoundByNameException(name)
        except LocationAlreadyExistsException:
            raise LocationIsNotUniqueException(payload.name)
        return LocationOut.model_validate(location_model)
    
    async def destroy(self, DataBase: AsyncSession, name: str):
        try:
            await self._repo.destroy(DataBase, name)
        except LocationNotFoundException:
            raise LocationNotFoundByNameException(name)