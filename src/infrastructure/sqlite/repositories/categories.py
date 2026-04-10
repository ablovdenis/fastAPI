from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session

from ..models.category_models import CategoryModel
from ....schems.categories import CategoryUpdateAndCreate


class CategoryRepository:
    def __init__(self):
        pass

    def get(self, DataBase: Session, skip: int, limit: int) -> List[CategoryModel]:
        return DataBase.query(CategoryModel).offset(skip).limit(limit).all()

    def get_detail(self, DataBase: Session, category_slug: str) -> CategoryModel:
        category = DataBase.query(CategoryModel).filter(
            CategoryModel.slug == category_slug
        ).first()
        if not category:
            raise HTTPException(status_code=404, detail='Категория не существует.')
        return category

    def create(self, DataBase: Session, payload: CategoryUpdateAndCreate) -> CategoryModel:
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

    def update(self, DataBase: Session, category_slug: str, payload: CategoryUpdateAndCreate) -> CategoryModel:
        category = DataBase.query(CategoryModel).filter(
            CategoryModel.slug == category_slug
        ).first()
        if not category:
            raise HTTPException(status_code=404, detail='Категория не существует.')
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(category, field, value)
        DataBase.commit()
        DataBase.refresh(category)
        return category

    def destroy(self, DataBase: Session, category_slug: str):
        category = DataBase.query(CategoryModel).filter(
            CategoryModel.slug == category_slug
        ).first()
        if not category:
            raise HTTPException(status_code=404, detail='Категория не существует.')
        DataBase.delete(category)
        DataBase.commit()