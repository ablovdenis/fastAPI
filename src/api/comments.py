import logging
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.schems.users import UserOut
from src.services.auth import get_current_user

from ..domain.comments.use_cases.crud_comments import MethodsForComment

from ..infrastructure.postgre.database import get_db
from ..schems.comments import CommentCreate, CommentOut, CommentUpdate

from src.core.exceptions.domain_exceptions import (CommentDontChangeException, CommentDontDestroyException, CommentNotFoundByIDException,
                                                   CommentDontCreateException,
                                                   PostNotFoundByIDException)

logger = logging.getLogger(__name__)

router = APIRouter(prefix='/comments', tags=['Комментарии'])


@router.get('/', response_model=List[CommentOut],
            summary='Комментарии:')
def list_comments(
    post_id: int | None = None,
    skip: int = 0,
    limit: int = 50,
    DataBase: Session = Depends(get_db),
) -> List[CommentOut]:
    logger.info(f"Запрос списка комментариев: post_id={post_id}, skip={skip}, limit={limit}")
    use_case = MethodsForComment()
    try:
        result = use_case.get(DataBase, post_id, skip, limit)
        logger.info(f"Возвращено {len(result)} комментариев")
        return result
    except PostNotFoundByIDException as e:
        logger.warning(f"Ошибка получения комментариев: пост с post_id={post_id} не найден")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail())


@router.get('/{comment_id}', response_model=CommentOut,
            summary='Получить комментарий:')
def get_comment(comment_id: int, DataBase: Session = Depends(get_db)) -> CommentOut:
    logger.info(f"Запрос комментария с id={comment_id}")
    use_case = MethodsForComment()
    try:
        result = use_case.get_detail(DataBase, comment_id)
        logger.info(f"Комментарий id={comment_id} найден")
        return result
    except CommentNotFoundByIDException as e:
        logger.warning(f"Комментарий с id={comment_id} не найден")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail())


@router.post('/', response_model=CommentOut,
             status_code=status.HTTP_201_CREATED,
             summary='Создать комментарий:')
def create_comment(payload: CommentCreate, DataBase: Session = Depends(get_db),
                   user: UserOut = Depends(get_current_user)) -> CommentOut:
    logger.info(f"Попытка создания комментария для поста post_id={payload.post_id} от пользователя id={user.id}")
    use_case = MethodsForComment()
    try:
        result = use_case.create(DataBase, payload, user.id)
        logger.info(f"Комментарий создан: id={result.id}")
        return result
    except CommentDontCreateException as e:
        logger.warning(f"Ошибка создания комментария: пост post_id={payload.post_id} не найден или другая причина")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail())


@router.put('/{comment_id}', response_model=CommentOut,
            summary='Изменить комментарий:')
def update_comment(comment_id: int, payload: CommentUpdate,
                   DataBase: Session = Depends(get_db),
                   user: UserOut = Depends(get_current_user)) -> CommentOut:
    logger.info(f"Попытка обновления комментария id={comment_id} от пользователя id={user.id}")
    use_case = MethodsForComment()
    try:
        result = use_case.update(DataBase, comment_id, payload, user.id)
        logger.info(f"Комментарий id={comment_id} обновлён")
        return result
    except CommentNotFoundByIDException as e:
        logger.warning(f"Ошибка обновления: комментарий id={comment_id} не найден")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail())
    except CommentDontChangeException as e:
        logger.warning(f"Ошибка обновления: пользователь id={user.id} не является автором комментария id={comment_id}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=e.get_detail())


@router.delete('/{comment_id}', status_code=status.HTTP_204_NO_CONTENT,
               summary='Удалить комментарий:')
def delete_comment(comment_id: int, DataBase: Session = Depends(get_db),
                   user: UserOut = Depends(get_current_user)):
    logger.info(f"Попытка удаления комментария id={comment_id} от пользователя id={user.id}")
    use_case = MethodsForComment()
    try:
        use_case.destroy(DataBase, comment_id, user.id)
        logger.info(f"Комментарий id={comment_id} удалён")
    except CommentNotFoundByIDException as e:
        logger.warning(f"Ошибка удаления: комментарий id={comment_id} не найден")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail())
    except CommentDontDestroyException as e:
        logger.warning(f"Ошибка удаления: пользователь id={user.id} не является автором комментария id={comment_id}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=e.get_detail())