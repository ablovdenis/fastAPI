from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ..domain.categories.use_cases.crud_categories import MethodsForCategory

from ..infrastructure.sqlite.database import get_db
from ..infrastructure.sqlite.models.category_models import CategoryModel
from ..schems.categories import CategoryOut, CategoryUpdateAndCreate

router = APIRouter(prefix='/categories', tags=['Категории постов'])


@router.get('/', response_model=List[CategoryOut],
            summary='Категории:')
def list_categories(skip: int = 0, limit: int = 10,
                    DataBase: Session = Depends(get_db)) -> List[CategoryOut]:
    use_case = MethodsForCategory()
    return use_case.get(DataBase, skip, limit)


@router.get('/{category_slug}', response_model=CategoryOut,
            summary='Получить категорию:')
def get_category(category_slug: str, DataBase: Session = Depends(get_db)) -> CategoryOut:
    use_case = MethodsForCategory()
    return use_case.get_detail(DataBase, category_slug)


@router.post('/', response_model=CategoryOut,
             status_code=status.HTTP_201_CREATED,
             summary='Создать категорию:')
def create_category(payload: CategoryUpdateAndCreate,
                    DataBase: Session = Depends(get_db)) -> CategoryOut:
    use_case = MethodsForCategory()
    return use_case.create(DataBase, payload)


@router.put('/{category_slug}', response_model=CategoryOut,
            summary='Изменить категорию:')
def update_category(category_slug: str, payload: CategoryUpdateAndCreate,
                    DataBase: Session = Depends(get_db)) -> CategoryOut:
    use_case = MethodsForCategory()
    return use_case.update(DataBase, category_slug, payload)


@router.delete('/{category_slug}', status_code=status.HTTP_204_NO_CONTENT,
               summary='Удалить категорию:')
def delete_category(category_slug: str, DataBase: Session = Depends(get_db)):
    use_case = MethodsForCategory()
    use_case.destroy(DataBase, category_slug)
