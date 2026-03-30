from typing import List

from sqlalchemy.orm import Session

from ....infrastructure.sqlite.repositories.locations import LocationRepository
from ....schems.locations import LocationOut, LocationUpdateAndCreate



class MethodsForLocation:
    def __init__(self):
        self._repo = LocationRepository()

    def get(self, DataBase: Session, skip: int, limit: int) -> List[LocationOut]:
        return [LocationOut.model_validate(user) for user in self._repo.get(DataBase, skip, limit)]

    def get_detail(self, DataBase: Session, location_id: int) -> LocationOut:
        return LocationOut.model_validate(self._repo.get_detail(DataBase, location_id))

    def create(self, DataBase: Session, payload: LocationUpdateAndCreate) -> LocationOut:
        return LocationOut.model_validate(self._repo.create(DataBase, payload))

    def update(self, DataBase: Session, location_id: int, payload: LocationUpdateAndCreate) -> LocationOut:
        return LocationOut.model_validate(self._repo.update(DataBase, location_id, payload))
    
    def destroy(self, DataBase: Session, location_id: int):
        self._repo.destroy(DataBase, location_id)