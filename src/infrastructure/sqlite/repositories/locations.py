from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session

from ..models.LocationModels import LocationModel
from ....schems.locations import LocationUpdateAndCreate


class LocationRepository:
    def __init__(self):
        pass

    def get(self, DataBase: Session, skip: int, limit: int) -> List[LocationModel]:
        return DataBase.query(LocationModel).offset(skip).limit(limit).all()

    def get_detail(self, DataBase: Session, location_id: int) -> LocationModel:
        location = DataBase.query(LocationModel).filter(
            LocationModel.id == location_id
        ).first()
        if not location:
            raise HTTPException(status_code=404,
                                detail='Местоположение не существует.')
        return location

    def create(self, DataBase: Session, payload: LocationUpdateAndCreate) -> LocationModel:
        location = LocationModel(**payload.model_dump())
        DataBase.add(location)
        DataBase.commit()
        DataBase.refresh(location)
        return location

    def update(self, DataBase: Session, location_id: int, payload: LocationUpdateAndCreate) -> LocationModel:
        location = DataBase.query(LocationModel).filter(
            LocationModel.id == location_id
        ).first()
        if not location:
            raise HTTPException(status_code=404,
                                detail='Местоположение не существует.')
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(location, field, value)
        DataBase.commit()
        DataBase.refresh(location)
        return location

    def destroy(self, DataBase: Session, location_id: int):
        location = DataBase.query(LocationModel).filter(
            LocationModel.id == location_id
        ).first()
        if not location:
            raise HTTPException(status_code=404,
                                detail='Местоположение не существует.')
        DataBase.delete(location)
        DataBase.commit()