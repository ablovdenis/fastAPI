from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session

from ..models.comment_models import CommentModel
from ..models.post_models import PostModel
from ..models.user_models import UserModel
from ....schems.comments import CommentCreate, CommentUpdate


class CommentRepository:
    def __init__(self):
        pass

    def get(self, DataBase: Session, post_id: int | None, skip: int, limit: int) -> List[CommentModel]:
        query = DataBase.query(CommentModel)
        if post_id is not None:
            query = query.filter(CommentModel.post_id == post_id)
        return query.order_by(CommentModel.created_at).offset(skip).limit(limit).all()

    def get_detail(self, DataBase: Session, comment_id: int) -> CommentModel:
        comment = DataBase.query(CommentModel).filter(
            CommentModel.id == comment_id
        ).first()
        if not comment:
            raise HTTPException(status_code=404, detail='Комментарий не существует.')
        return comment

    def create(self, DataBase: Session, payload: CommentCreate) -> CommentModel:
        post = DataBase.query(PostModel).filter(
            PostModel.id == payload.post_id
        ).first()
        if not post:
            raise HTTPException(status_code=404, detail='Публикация не существует.')
        author = DataBase.query(UserModel).filter(
            UserModel.id == payload.author_id
        ).first()
        if not author:
            raise HTTPException(status_code=404, detail='Автор не существует.')

        comment = CommentModel(**payload.model_dump())
        DataBase.add(comment)
        DataBase.commit()
        DataBase.refresh(comment)
        return comment

    def update(self, DataBase: Session, comment_id: int, payload: CommentUpdate) -> CommentModel:
        comment = DataBase.query(CommentModel).filter(
            CommentModel.id == comment_id
        ).first()
        if not comment:
            raise HTTPException(status_code=404, detail='Комментарий не существует.')
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(comment, field, value)
        DataBase.commit()
        DataBase.refresh(comment)
        return comment

    def destroy(self, DataBase: Session, comment_id: int):
        comment = DataBase.query(CommentModel).filter(
            CommentModel.id == comment_id
        ).first()
        if not comment:
            raise HTTPException(status_code=404, detail='Комментарий не существует.')
        DataBase.delete(comment)
        DataBase.commit()