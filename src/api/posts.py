from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.services.auth import get_current_user

from ..schems.users import UserOut

from ..domain.posts.use_cases.crud_posts import MethodsForPost

from src.core.exceptions.domain_exceptions import (PostDontDestroyException, PostNotFoundByIDException,
                                                   PostDontCreateException,
                                                   PostDontChangeException)

from ..infrastructure.sqlite.database import get_db
from ..schems.posts import PostCreateAndUpdate, PostDetail, PostOut

router = APIRouter(prefix='/posts', tags=['Посты'])


@router.get('/all', response_model=List[PostOut],
            summary='Публикации:')
def list_posts(
    skip: int = 0,
    limit: int = 20,
    published_only: bool = False,
    DataBase: Session = Depends(get_db)
) -> List[PostOut]:
    use_case = MethodsForPost()
    return use_case.get(DataBase, skip, limit, published_only)


@router.get('/{post_id}', response_model=PostDetail,
            summary='Получить публикацию:')
def get_post(post_id: int, DataBase: Session = Depends(get_db)) -> PostDetail:
    use_case = MethodsForPost()
    try:
        return use_case.get_detail(DataBase, post_id)
    except PostNotFoundByIDException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail())


@router.post('/', response_model=PostOut,
             status_code=status.HTTP_201_CREATED,
             summary='Создать публикацию:')
def create_post(payload: PostCreateAndUpdate, DataBase: Session = Depends(get_db),
                user: UserOut = Depends(get_current_user)) -> PostOut:
    use_case = MethodsForPost()
    try:
        return use_case.create(DataBase, payload, user.nickname)
    except PostDontCreateException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail())


@router.put('/{post_id}', response_model=PostOut,
            summary='Изменить публикацию:')
def update_post(post_id: int, payload: PostCreateAndUpdate,
                DataBase: Session = Depends(get_db),
                user: UserOut = Depends(get_current_user)) -> PostOut:
    use_case = MethodsForPost()
    try:
        return use_case.update(DataBase, payload, post_id, user.id)
    except PostNotFoundByIDException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail())
    except PostDontChangeException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=e.get_detail())


@router.delete('/{post_id}', status_code=status.HTTP_204_NO_CONTENT,
               summary='Удалить публикацию:')
def delete_post(post_id: int, DataBase: Session = Depends(get_db),
                user: UserOut = Depends(get_current_user)):
    use_case = MethodsForPost()
    try:
        use_case.destroy(DataBase, post_id, user.id)
    except PostNotFoundByIDException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail())
    except PostDontDestroyException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=e.get_detail())
