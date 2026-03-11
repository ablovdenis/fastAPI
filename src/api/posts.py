from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload

from ..domain.posts.use_cases.MethodsForPost import MethodsForPost

from ..infrastructure.sqlite.configSQL import get_db
from ..infrastructure.sqlite.models.CategoryModels import CategoryModel
from ..infrastructure.sqlite.models.LocationModels import LocationModel
from ..infrastructure.sqlite.models.PostModels import PostModel
from ..infrastructure.sqlite.models.UserModels import UserModel
from ..schems.posts import PostCreate, PostDetail, PostOut, PostUpdate

router = APIRouter(prefix='/posts', tags=['Посты'])


@router.get('/', response_model=List[PostOut],
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
    return use_case.get_detail(DataBase, post_id)


@router.post('/', response_model=PostOut,
             status_code=status.HTTP_201_CREATED,
             summary='Создать публикацию:')
def create_post(payload: PostCreate, DataBase: Session = Depends(get_db)) -> PostOut:
    use_case = MethodsForPost()
    return use_case.create(DataBase, payload)


@router.put('/{post_id}', response_model=PostOut,
            summary='Изменить публикацию:')
def update_post(post_id: int, payload: PostUpdate,
                DataBase: Session = Depends(get_db)) -> PostOut:
    use_case = MethodsForPost()
    return use_case.update(DataBase, post_id, payload)


@router.delete('/{post_id}', status_code=status.HTTP_204_NO_CONTENT,
               summary='Удалить публикацию:')
def delete_post(post_id: int, DataBase: Session = Depends(get_db)):
    use_case = MethodsForPost()
    use_case.destroy(DataBase, post_id)
