from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..domain.comments.use_cases.MethodsForComment import MethodsForComment

from ..infrastructure.sqlite.configSQL import get_db
from ..infrastructure.sqlite.models.CommentModels import CommentModel
from ..infrastructure.sqlite.models.PostModels import PostModel
from ..infrastructure.sqlite.models.UserModels import UserModel
from ..schems.comments import CommentCreate, CommentOut, CommentUpdate

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
    return use_case.get(DataBase, post_id, skip, limit)


@router.get('/{comment_id}', response_model=CommentOut,
            summary='Получить комментарий:')
def get_comment(comment_id: int, DataBase: Session = Depends(get_db)) -> CommentOut:
    use_case = MethodsForComment()
    return use_case.get_detail(DataBase, comment_id)


@router.post('/', response_model=CommentOut,
             status_code=status.HTTP_201_CREATED,
             summary='Создать комментарий:')
def create_comment(payload: CommentCreate,
                   DataBase: Session = Depends(get_db)) -> CommentOut:
    use_case = MethodsForComment()
    return use_case.create(DataBase, payload)


@router.put('/{comment_id}', response_model=CommentOut,
            summary='Изменить комментарий:')
def update_comment(comment_id: int, payload: CommentUpdate,
                   DataBase: Session = Depends(get_db)) -> CommentOut:
    use_case = MethodsForComment()
    return use_case.update(DataBase, comment_id, payload)


@router.delete('/{comment_id}', status_code=status.HTTP_204_NO_CONTENT,
               summary='Удалить комментарий:')
def delete_comment(comment_id: int, DataBase: Session = Depends(get_db)):
    use_case = MethodsForComment()
    use_case.destroy(DataBase, comment_id)
