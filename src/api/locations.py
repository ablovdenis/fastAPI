from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..domain.locations.use_cases.crud_locations import MethodsForLocation

from ..infrastructure.sqlite.database import get_db
from ..infrastructure.sqlite.models.location_models import LocationModel
from ..schems.locations import LocationOut, LocationUpdateAndCreate

router = APIRouter(prefix='/locations', tags=['Местоположения'])


@router.get('/', response_model=List[LocationOut],
            summary='Местоположения:')
def list_locations(skip: int = 0, limit: int = 20,
                   DataBase: Session = Depends(get_db)) -> List[LocationOut]:
    use_case = MethodsForLocation()
    return use_case.get(DataBase, skip, limit)


@router.get('/{name}', response_model=LocationOut,
            summary='Получить местоположение:')
def get_location(name: str, DataBase: Session = Depends(get_db)) -> LocationOut:
    use_case = MethodsForLocation()
    return use_case.get_detail(DataBase, name)


@router.post('/', response_model=LocationOut,
             status_code=status.HTTP_201_CREATED,
             summary='Создать местоположение:')
def create_location(payload: LocationUpdateAndCreate,
                    DataBase: Session = Depends(get_db)) -> LocationOut:
    use_case = MethodsForLocation()
    return use_case.create(DataBase, payload)


@router.put('/{name}', response_model=LocationOut,
            summary='Сменить местоположение:')
def update_location(name: str, payload: LocationUpdateAndCreate,
                    DataBase: Session = Depends(get_db)) -> LocationOut:
    use_case = MethodsForLocation()
    return use_case.update(DataBase, name, payload)


@router.delete('/{name}', status_code=status.HTTP_204_NO_CONTENT,
               summary='Удалить местоположение:')
def delete_location(name: str, DataBase: Session = Depends(get_db)):
    use_case = MethodsForLocation()
    use_case.destroy(DataBase, name)
