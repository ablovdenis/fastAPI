from typing import List

from sqlalchemy.orm import Session, joinedload

from ..models.category_models import CategoryModel
from ..models.location_models import LocationModel
from ..models.post_models import PostModel
from ..models.user_models import UserModel
from ....schems.posts import PostCreateAndUpdate

from src.core.exceptions.database_exceptions import (CredentialException, UserNotFoundException,
                                                     CategoryNotFoundException,
                                                     LocationNotFoundException, 
                                                     PostNotFoundException)

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
            raise PostNotFoundException()
        return post

    def create(self, DataBase: Session, payload: PostCreateAndUpdate,
               nickname: str) -> PostModel:
        author = DataBase.query(UserModel).filter(
            UserModel.nickname == nickname
        ).first()
        if not author:
            raise UserNotFoundException()

        category = DataBase.query(CategoryModel).filter(
            CategoryModel.slug == payload.category_slug
        ).first()
        if not category:
            raise CategoryNotFoundException()

        location = DataBase.query(LocationModel).filter(
            LocationModel.name == payload.location_name
        ).first()
        if not location:
            raise LocationNotFoundException()

        dict_ = (payload.model_dump(
                    exclude={'location_name',
                             'author_nickname',
                             'category_slug'}
                    ) |
                 {'location_id':location.id,
                  'category_id':category.id,
                  'author_id':author.id})
        post = PostModel(**dict_)
        DataBase.add(post)
        DataBase.commit()
        DataBase.refresh(post)
        return post

    def update_without_image(self, DataBase: Session, payload: PostCreateAndUpdate,
               post_id: int, nickname: str) -> PostModel:
        post = DataBase.query(PostModel).filter(PostModel.id == post_id).first()
        if not post:
            raise PostNotFoundException()
        
        user_by_nickname = DataBase.query(UserModel).filter(
            UserModel.nickname == nickname
        ).first()
        if post.author_id != user_by_nickname.id:
            raise CredentialException()

        dop_dict = {}

        if payload.category_slug:
            category = DataBase.query(CategoryModel).filter(
                CategoryModel.slug == payload.category_slug
            ).first()
            if not category:
                raise CategoryNotFoundException()
            dop_dict['category_id'] = category.id

        if payload.location_name:
            location = DataBase.query(LocationModel).filter(
                LocationModel.name == payload.location_name
            ).first()
            if not location:
                raise LocationNotFoundException()
            dop_dict['location_id'] = location.id

        dict_ = (payload.model_dump(
                    exclude={'location_name',
                             'author_nickname',
                             'category_slug'}
                    ) | dop_dict)

        for field, value in dict_.items():
            setattr(post, field, value)
        DataBase.commit()
        DataBase.refresh(post)
        return post

    def update_image(self, DataBase: Session, image: str,
               post_id: int, nickname: int) -> PostModel:
        post = DataBase.query(PostModel).filter(PostModel.id == post_id).first()
        if not post:
            raise PostNotFoundException()
        
        user_by_nickname = DataBase.query(UserModel).filter(
            UserModel.nickname == nickname
        ).first()
        if post.author_id != user_by_nickname.id:
            raise CredentialException()

        post.image = image

        DataBase.commit()
        DataBase.refresh(post)
        return post

    def destroy(self, DataBase: Session, post_id: int, nickname: str):
        post = DataBase.query(PostModel).filter(PostModel.id == post_id).first()
        if not post:
            raise PostNotFoundException()
        user_by_nickname = DataBase.query(UserModel).filter(
            UserModel.nickname == nickname
        ).first()
        if post.author_id != user_by_nickname.id:
            raise CredentialException()
        DataBase.delete(post)
        DataBase.commit()