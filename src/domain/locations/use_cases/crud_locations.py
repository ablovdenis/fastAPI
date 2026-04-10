from typing import List

from sqlalchemy.orm import Session

from ....infrastructure.sqlite.repositories.locations import LocationRepository
from ....schems.locations import LocationOut, LocationUpdateAndCreate



class MethodsForLocation:
    def __init__(self):
        self._repo = LocationRepository()

    def get(self, DataBase: Session, skip: int, limit: int) -> List[LocationOut]:
        return [LocationOut.model_validate(user) for user in self._repo.get(DataBase, skip, limit)]

    def get_detail(self, DataBase: Session, name: str) -> LocationOut:
        return LocationOut.model_validate(self._repo.get_detail(DataBase, name))

    def create(self, DataBase: Session, payload: LocationUpdateAndCreate) -> LocationOut:
        return LocationOut.model_validate(self._repo.create(DataBase, payload))

    def update(self, DataBase: Session, name: str, payload: LocationUpdateAndCreate) -> LocationOut:
        return LocationOut.model_validate(self._repo.update(DataBase, name, payload))
    
    def destroy(self, DataBase: Session, name: str):
        self._repo.destroy(DataBase, name)