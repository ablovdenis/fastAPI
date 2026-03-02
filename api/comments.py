from data_base.configSQL import *
from schems.comments import *

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter(prefix='/comments', tags=['Комментарии'])


@router.get('/', response_model=List[CommentOut],
            summary='Комментарии:')
def list_comments(
    post_id: int | None = None,
    skip: int = 0,
    limit: int = 50,
    DataBase: Session = Depends(get_db),
):
    query = DataBase.query(CommentModel)
    if post_id is not None:
        query = query.filter(CommentModel.post_id == post_id)
    return query.order_by(CommentModel.created_at).offset(skip).limit(limit).all()


@router.get('/{comment_id}', response_model=CommentOut,
            summary='Получить комментарий:')
def get_comment(comment_id: int, DataBase: Session = Depends(get_db)):
    comment = DataBase.query(CommentModel).filter(
        CommentModel.id == comment_id
    ).first()
    if not comment:
        raise HTTPException(status_code=404, detail='Комментарий не существует.')
    return comment


@router.post('/', response_model=CommentOut,
             status_code=status.HTTP_201_CREATED,
             summary='Создать комментарий:')
def create_comment(payload: CommentCreate,
                   DataBase: Session = Depends(get_db)):
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


@router.put('/{comment_id}', response_model=CommentOut,
            summary='Изменить комментарий:')
def update_comment(comment_id: int, payload: CommentUpdate,
                   DataBase: Session = Depends(get_db)):
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


@router.delete('/{comment_id}', status_code=status.HTTP_204_NO_CONTENT,
               summary='Удалить комментарий:')
def delete_comment(comment_id: int, DataBase: Session = Depends(get_db)):
    comment = DataBase.query(CommentModel).filter(
        CommentModel.id == comment_id
    ).first()
    if not comment:
        raise HTTPException(status_code=404, detail='Комментарий не существует.')
    DataBase.delete(comment)
    DataBase.commit()
