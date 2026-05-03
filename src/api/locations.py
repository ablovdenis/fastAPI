import logging

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.schems.users import UserOut
from src.services.auth import get_current_user

from ..domain.locations.use_cases.crud_locations import MethodsForLocation

from src.core.exceptions.domain_exceptions import LocationNotFoundByNameException, LocationIsNotUniqueException

from ..infrastructure.postgre.database import get_db
from ..schems.locations import LocationOut, LocationUpdateAndCreate

logger = logging.getLogger(__name__)

router = APIRouter(prefix='/locations', tags=['Местоположения'])


@router.get('/', response_model=List[LocationOut],
            summary='Местоположения:')
def list_locations(skip: int = 0, limit: int = 20,
                   DataBase: Session = Depends(get_db)) -> List[LocationOut]:
    logger.info(f"Запрос списка локаций: skip={skip}, limit={limit}")
    use_case = MethodsForLocation()
    result = use_case.get(DataBase, skip, limit)
    logger.info(f"Возвращено {len(result)} локаций")
    return result


@router.get('/{name}', response_model=LocationOut,
            summary='Получить местоположение:')
def get_location(name: str, DataBase: Session = Depends(get_db)) -> LocationOut:
    logger.info(f"Запрос локации по имени='{name}'")
    use_case = MethodsForLocation()
    try:
        result = use_case.get_detail(DataBase, name)
        logger.info(f"Локация '{name}' найдена")
        return result
    except LocationNotFoundByNameException as e:
        logger.warning(f"Локация '{name}' не найдена")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail())


@router.post('/', response_model=LocationOut,
             status_code=status.HTTP_201_CREATED,
             summary='Создать местоположение:')
def create_location(payload: LocationUpdateAndCreate,
                    DataBase: Session = Depends(get_db),
                    _: UserOut = Depends(get_current_user)) -> LocationOut:
    logger.info(f"Попытка создания локации с именем='{payload.name}'")
    use_case = MethodsForLocation()
    try:
        result = use_case.create(DataBase, payload)
        logger.info(f"Локация создана: id={result.id}, name='{result.name}'")
        return result
    except LocationIsNotUniqueException as e:
        logger.warning(f"Ошибка создания локации: имя '{payload.name}' уже существует")
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=e.get_detail())


@router.put('/{name}', response_model=LocationOut,
            summary='Сменить местоположение:')
def update_location(name: str, payload: LocationUpdateAndCreate,
                    DataBase: Session = Depends(get_db),
                    _: UserOut = Depends(get_current_user)) -> LocationOut:
    logger.info(f"Попытка обновления локации с именем='{name}'")
    use_case = MethodsForLocation()
    try:
        result = use_case.update(DataBase, name, payload)
        logger.info(f"Локация обновлена: старое имя='{name}', новое имя='{result.name}'")
        return result
    except LocationNotFoundByNameException as e:
        logger.warning(f"Ошибка обновления: локация с именем='{name}' не найдена")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail())
    except LocationIsNotUniqueException as e:
        logger.warning(f"Ошибка обновления: новое имя '{payload.name}' уже существует")
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=e.get_detail())


@router.delete('/{name}', status_code=status.HTTP_204_NO_CONTENT,
               summary='Удалить местоположение:')
def delete_location(name: str, DataBase: Session = Depends(get_db),
                    _: UserOut = Depends(get_current_user)):
    logger.info(f"Попытка удаления локации с именем='{name}'")
    use_case = MethodsForLocation()
    try:
        use_case.destroy(DataBase, name)
        logger.info(f"Локация '{name}' удалена")
    except LocationNotFoundByNameException as e:
        logger.warning(f"Ошибка удаления: локация '{name}' не найдена")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail())