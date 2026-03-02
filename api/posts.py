from data_base.configSQL import *
from schems.posts import *

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload

router = APIRouter(prefix='/posts', tags=['Посты'])


@router.get('/', response_model=List[PostOut],
            summary='Публикации:')
def list_posts(
    skip: int = 0,
    limit: int = 20,
    published_only: bool = False,
    DataBase: Session = Depends(get_db),
):
    query = DataBase.query(PostModel)
    if published_only:
        query = query.filter(PostModel.is_published.is_(True))
    return query.order_by(PostModel.pub_date.desc()).offset(skip).limit(limit).all()


@router.get('/{post_id}', response_model=PostDetail,
            summary='Получить публикацию:')
def get_post(post_id: int, DataBase: Session = Depends(get_db)):
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


@router.post('/', response_model=PostOut,
             status_code=status.HTTP_201_CREATED,
             summary='Создать публикацию:')
def create_post(payload: PostCreate, DataBase: Session = Depends(get_db)):
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


@router.put('/{post_id}', response_model=PostOut,
            summary='Изменить публикацию:')
def update_post(post_id: int, payload: PostUpdate,
                DataBase: Session = Depends(get_db)):
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


@router.delete('/{post_id}', status_code=status.HTTP_204_NO_CONTENT,
               summary='Удалить публикацию:')
def delete_post(post_id: int, DataBase: Session = Depends(get_db)):
    post = DataBase.query(PostModel).filter(PostModel.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail='Публикация не существует.')
    DataBase.delete(post)
    DataBase.commit()
