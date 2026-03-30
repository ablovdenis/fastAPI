from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload

from ..models.CategoryModels import CategoryModel
from ..models.LocationModels import LocationModel
from ..models.PostModels import PostModel
from ..models.UserModels import UserModel
from ....schems.posts import PostCreate, PostUpdate


class PostRepository:
    def __init__(self):
        pass

    def get(self, DataBase: Session,
            skip: int,
            limit: int,
            published_only: bool) -> List[PostModel]:
        query = DataBase.query(PostModel)
        if published_only:
            query = query.filter(PostModel.is_published.is_(True))
        return query.order_by(PostModel.pub_date.desc()).offset(skip).limit(limit).all()

    def get_detail(self, DataBase: Session, post_id: int) -> PostModel:
        post = (
            DataBase.query(PostModel)
            .options(
                joinedload(PostModel.author),
                joinedload(PostModel.category),
                joinedload(PostModel.location),
                joinedload(PostModel.comments),
            )
            .filter(PostModel.id == post_id)
            .first()
        )
        if not post:
            raise HTTPException(status_code=404, detail='Публикация не существует.')
        return post

    def create(self, DataBase: Session, payload: PostCreate) -> PostModel:
        author = DataBase.query(UserModel).filter(
            UserModel.id == payload.author_id
        ).first()
        if not author:
            raise HTTPException(status_code=404, detail='Автор не существует.')
        
        categori = DataBase.query(CategoryModel).filter(
            CategoryModel.id == payload.category_id
        ).first()
        if not categori:
            raise HTTPException(status_code=404, detail='Категория не существует.')

        location = DataBase.query(LocationModel).filter(
            LocationModel.id == payload.location_id
        ).first()
        if not location:
            raise HTTPException(status_code=404, detail='Локация не существует.')

        post = PostModel(**payload.model_dump())
        DataBase.add(post)
        DataBase.commit()
        DataBase.refresh(post)
        return post

    def update(self, DataBase: Session, post_id: int, payload: PostUpdate) -> PostModel:
        post = DataBase.query(PostModel).filter(PostModel.id == post_id).first()
        if not post:
            raise HTTPException(status_code=404, detail='Публикация не существует.')
        
        categori = DataBase.query(CategoryModel).filter(
            CategoryModel.id == payload.category_id
        ).first()
        if not categori:
            raise HTTPException(status_code=404, detail='Категория не существует.')

        location = DataBase.query(LocationModel).filter(
            LocationModel.id == payload.location_id
        ).first()
        if not location:
            raise HTTPException(status_code=404, detail='Локация не существует.')


        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(post, field, value)
        DataBase.commit()
        DataBase.refresh(post)
        return post

    def destroy(self, DataBase: Session, post_id: int):
        post = DataBase.query(PostModel).filter(PostModel.id == post_id).first()
        if not post:
            raise HTTPException(status_code=404, detail='Публикация не существует.')
        DataBase.delete(post)
        DataBase.commit()