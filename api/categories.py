from data_base.configSQL import *
from schems.categories import *

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter(prefix='/categories', tags=['Категории постов'])


@router.get('/', response_model=List[CategoryOut],
            summary='Категории:')
def list_categories(skip: int = 0, limit: int = 10,
                    DataBase: Session = Depends(get_db)):
    return DataBase.query(CategoryModel).offset(skip).limit(limit).all()


@router.get('/{category_id}', response_model=CategoryOut,
            summary='Получить категорию:')
def get_category(category_id: int, DataBase: Session = Depends(get_db)):
    category = DataBase.query(CategoryModel).filter(
        CategoryModel.id == category_id
    ).first()
    if not category:
        raise HTTPException(status_code=404, detail='Категория не существует.')
    return category


@router.post('/', response_model=CategoryOut,
             status_code=status.HTTP_201_CREATED,
             summary='Создать категорию:')
def create_category(payload: CategoryUpdateAndCreate,
                    DataBase: Session = Depends(get_db)):
    if DataBase.query(CategoryModel).filter(
        CategoryModel.slug == payload.slug
    ).first():
        raise HTTPException(status_code=400,
                            detail='Категория с таким идентификатором уже существует.')
    category = CategoryModel(**payload.model_dump())
    DataBase.add(category)
    DataBase.commit()
    DataBase.refresh(category)
    return category


@router.put('/{category_id}', response_model=CategoryOut,
            summary='Изменить категорию:')
def update_category(category_id: int, payload: CategoryUpdateAndCreate,
                    DataBase: Session = Depends(get_db)):
    category = DataBase.query(CategoryModel).filter(
        CategoryModel.id == category_id
    ).first()
    if not category:
        raise HTTPException(status_code=404, detail='Категория не существует.')
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(category, field, value)
    DataBase.commit()
    DataBase.refresh(category)
    return category


@router.delete('/{category_id}', status_code=status.HTTP_204_NO_CONTENT,
               summary='Удалить категорию:')
def delete_category(category_id: int, DataBase: Session = Depends(get_db)):
    category = DataBase.query(CategoryModel).filter(
        CategoryModel.id == category_id
    ).first()
    if not category:
        raise HTTPException(status_code=404, detail='Категория не существует.')
    DataBase.delete(category)
    DataBase.commit()
