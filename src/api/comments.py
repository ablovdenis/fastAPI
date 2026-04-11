from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..domain.comments.use_cases.crud_comments import MethodsForComment

from ..infrastructure.sqlite.database import get_db
from ..schems.comments import CommentCreate, CommentOut, CommentUpdate

from src.core.exceptions.domain_exceptions import (CommentNotFoundByIDException,
                                                   CommentDontCreateException,
                                                   PostNotFoundByIDException)

router = APIRouter(prefix='/comments', tags=['Комментарии'])


@router.get('/', response_model=List[CommentOut],
            summary='Комментарии:')
def list_comments(
    post_id: int | None = None,
    skip: int = 0,
    limit: int = 50,
    DataBase: Session = Depends(get_db),
) -> List[CommentOut]:
    use_case = MethodsForComment()
    try:
        return use_case.get(DataBase, post_id, skip, limit)
    except PostNotFoundByIDException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail())


@router.get('/{comment_id}', response_model=CommentOut,
            summary='Получить комментарий:')
def get_comment(comment_id: int, DataBase: Session = Depends(get_db)) -> CommentOut:
    use_case = MethodsForComment()
    try:
        return use_case.get_detail(DataBase, comment_id)
    except CommentNotFoundByIDException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail())


@router.post('/', response_model=CommentOut,
             status_code=status.HTTP_201_CREATED,
             summary='Создать комментарий:')
def create_comment(payload: CommentCreate,
                   DataBase: Session = Depends(get_db)) -> CommentOut:
    use_case = MethodsForComment()
    try:
        return use_case.create(DataBase, payload)
    except CommentDontCreateException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail())


@router.put('/{comment_id}', response_model=CommentOut,
            summary='Изменить комментарий:')
def update_comment(comment_id: int, payload: CommentUpdate,
                   DataBase: Session = Depends(get_db)) -> CommentOut:
    use_case = MethodsForComment()
    try:
        return use_case.update(DataBase, comment_id, payload)
    except CommentNotFoundByIDException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail())


@router.delete('/{comment_id}', status_code=status.HTTP_204_NO_CONTENT,
               summary='Удалить комментарий:')
def delete_comment(comment_id: int, DataBase: Session = Depends(get_db)):
    use_case = MethodsForComment()
    try:
        use_case.destroy(DataBase, comment_id)
    except CommentNotFoundByIDException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail())
