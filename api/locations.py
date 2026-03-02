from data_base.configSQL import *
from schems.locations import *

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter(prefix='/locations', tags=['Местоположения'])


@router.get('/', response_model=List[LocationOut],
            summary='Местоположения:')
def list_locations(skip: int = 0, limit: int = 20,
                   DataBase: Session = Depends(get_db)):
    return DataBase.query(LocationModel).offset(skip).limit(limit).all()


@router.get('/{location_id}', response_model=LocationOut,
            summary='Получить местоположение:')
def get_location(location_id: int, DataBase: Session = Depends(get_db)):
    location = DataBase.query(LocationModel).filter(
        LocationModel.id == location_id
    ).first()
    if not location:
        raise HTTPException(status_code=404,
                            detail='Местоположение не существует.')
    return location


@router.post('/', response_model=LocationOut,
             status_code=status.HTTP_201_CREATED,
             summary='Создать местоположение:')
def create_location(payload: LocationUpdateAndCreate,
                    DataBase: Session = Depends(get_db)):
    location = LocationModel(**payload.model_dump())
    DataBase.add(location)
    DataBase.commit()
    DataBase.refresh(location)
    return location


@router.put('/{location_id}', response_model=LocationOut,
            summary='Сменить местоположение:')
def update_location(location_id: int, payload: LocationUpdateAndCreate,
                    DataBase: Session = Depends(get_db)):
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


@router.delete('/{location_id}', status_code=status.HTTP_204_NO_CONTENT,
               summary='Удалить местоположение:')
def delete_location(location_id: int, DataBase: Session = Depends(get_db)):
    location = DataBase.query(LocationModel).filter(
        LocationModel.id == location_id
    ).first()
    if not location:
        raise HTTPException(status_code=404,
                            detail='Местоположение не существует.')
    DataBase.delete(location)
    DataBase.commit()
