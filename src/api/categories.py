import logging
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.schems.users import UserOut
from src.services.auth import get_current_user

from ..domain.categories.use_cases.crud_categories import MethodsForCategory

from src.core.exceptions.domain_exceptions import CategoryNotFoundBySlugException, CategoryIsNotUniqueException

from ..infrastructure.postgre.database import get_db
from ..schems.categories import CategoryOut, CategoryUpdateAndCreate

logger = logging.getLogger(__name__)

router = APIRouter(prefix='/categories', tags=['Категории постов'])


@router.get('/', response_model=List[CategoryOut],
            summary='Категории:')
def list_categories(skip: int = 0, limit: int = 10,
                    DataBase: Session = Depends(get_db)) -> List[CategoryOut]:
    logger.info(f"Запрошен список категорий: skip={skip}, limit={limit}")
    use_case = MethodsForCategory()
    result = use_case.get(DataBase, skip, limit)
    logger.info(f"Возвращено {len(result)} категорий")
    return result


@router.get('/{category_slug}', response_model=CategoryOut,
            summary='Получить категорию:')
def get_category(category_slug: str, DataBase: Session = Depends(get_db)) -> CategoryOut:
    logger.info(f"Запрос категории с slug='{category_slug}'")
    use_case = MethodsForCategory()
    try:
        result = use_case.get_detail(DataBase, category_slug)
        logger.info(f"Категория с slug='{category_slug}' найдена")
        return result
    except CategoryNotFoundBySlugException as e:
        logger.warning(f"Категория с slug='{category_slug}' не найдена")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail())


@router.post('/', response_model=CategoryOut,
             status_code=status.HTTP_201_CREATED,
             summary='Создать категорию:')
def create_category(payload: CategoryUpdateAndCreate,
                    DataBase: Session = Depends(get_db),
                    _: UserOut = Depends(get_current_user)) -> CategoryOut:
    logger.info(f"Попытка создания категории с данными: slug='{payload.slug}', title='{payload.title}'")
    use_case = MethodsForCategory()
    try:
        result = use_case.create(DataBase, payload)
        logger.info(f"Категория создана: id={result.id}, slug='{result.slug}'")
        return result
    except CategoryIsNotUniqueException as e:
        logger.warning(f"Ошибка создания категории: slug '{payload.slug}' уже существует")
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=e.get_detail())


@router.put('/{category_slug}', response_model=CategoryOut,
            summary='Изменить категорию:')
def update_category(category_slug: str, payload: CategoryUpdateAndCreate,
                    DataBase: Session = Depends(get_db),
                    _: UserOut = Depends(get_current_user)) -> CategoryOut:
    logger.info(f"Попытка обновления категории slug='{category_slug}'")
    use_case = MethodsForCategory()
    try:
        result = use_case.update(DataBase, category_slug, payload)
        logger.info(f"Категория обновлена: slug='{result.slug}'")
        return result
    except CategoryNotFoundBySlugException as e:
        logger.warning(f"Ошибка обновления: категория с slug='{category_slug}' не найдена")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail())
    except CategoryIsNotUniqueException as e:
        logger.warning(f"Ошибка обновления: новый slug '{payload.slug}' уже существует")
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=e.get_detail())


@router.delete('/{category_slug}', status_code=status.HTTP_204_NO_CONTENT,
               summary='Удалить категорию:')
def delete_category(category_slug: str, DataBase: Session = Depends(get_db),
                    _: UserOut = Depends(get_current_user)):
    logger.info(f"Попытка удаления категории slug='{category_slug}'")
    use_case = MethodsForCategory()
    try:
        use_case.destroy(DataBase, category_slug)
        logger.info(f"Категория slug='{category_slug}' удалена")
    except CategoryNotFoundBySlugException as e:
        logger.warning(f"Ошибка удаления: категория slug='{category_slug}' не найдена")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail())