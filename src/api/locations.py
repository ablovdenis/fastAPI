from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..domain.locations.use_cases.MethodsForLocation import MethodsForLocation

from ..infrastructure.sqlite.configSQL import get_db
from ..infrastructure.sqlite.models.LocationModels import LocationModel
from ..schems.locations import LocationOut, LocationUpdateAndCreate

router = APIRouter(prefix='/locations', tags=['Местоположения'])


@router.get('/', response_model=List[LocationOut],
            summary='Местоположения:')
def list_locations(skip: int = 0, limit: int = 20,
                   DataBase: Session = Depends(get_db)) -> List[LocationOut]:
    use_case = MethodsForLocation()
    return use_case.get(DataBase, skip, limit)


@router.get('/{location_id}', response_model=LocationOut,
            summary='Получить местоположение:')
def get_location(location_id: int, DataBase: Session = Depends(get_db)) -> LocationOut:
    use_case = MethodsForLocation()
    return use_case.get_detail(DataBase, location_id)


@router.post('/', response_model=LocationOut,
             status_code=status.HTTP_201_CREATED,
             summary='Создать местоположение:')
def create_location(payload: LocationUpdateAndCreate,
                    DataBase: Session = Depends(get_db)) -> LocationOut:
    use_case = MethodsForLocation()
    return use_case.create(DataBase, payload)


@router.put('/{location_id}', response_model=LocationOut,
            summary='Сменить местоположение:')
def update_location(location_id: int, payload: LocationUpdateAndCreate,
                    DataBase: Session = Depends(get_db)) -> LocationOut:
    use_case = MethodsForLocation()
    return use_case.update(DataBase, location_id, payload)


@router.delete('/{location_id}', status_code=status.HTTP_204_NO_CONTENT,
               summary='Удалить местоположение:')
def delete_location(location_id: int, DataBase: Session = Depends(get_db)):
    use_case = MethodsForLocation()
    use_case.destroy(DataBase, location_id)
