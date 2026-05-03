import logging

from typing import List
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from src.services.auth import get_current_user

from ..schems.users import UserOut

from ..domain.posts.use_cases.crud_image import MethodsForImage
from ..domain.posts.use_cases.crud_posts import MethodsForPost

from src.core.exceptions.domain_exceptions import (ImageDontDestroyException, IsNotAnImageExtensionException, PostDontDestroyException, PostHasNoImageException, PostNotFoundByIDException,
                                                   PostDontCreateException,
                                                   PostDontChangeException)

from ..infrastructure.postgre.database import get_db
from ..schems.posts import PostCreateAndUpdate, PostDetail, PostImage, PostOut

logger = logging.getLogger(__name__)

router = APIRouter(prefix='/posts', tags=['Посты'])


@router.get('/all', response_model=List[PostOut],
            summary='Публикации:')
def list_posts(
    skip: int = 0,
    limit: int = 20,
    published_only: bool = False,
    DataBase: Session = Depends(get_db)
) -> List[PostOut]:
    logger.info(f"Запрос списка постов: skip={skip}, limit={limit}, published_only={published_only}")
    use_case = MethodsForPost()
    result = use_case.get(DataBase, skip, limit, published_only)
    logger.info(f"Возвращено {len(result)} постов")
    return result


@router.get('/{post_id}', response_model=PostDetail,
            summary='Получить публикацию:')
def get_post(post_id: int, DataBase: Session = Depends(get_db)) -> PostDetail:
    logger.info(f"Запрос поста с id={post_id}")
    use_case = MethodsForPost()
    try:
        result = use_case.get_detail(DataBase, post_id)
        logger.info(f"Пост id={post_id} найден")
        return result
    except PostNotFoundByIDException as e:
        logger.warning(f"Пост id={post_id} не найден")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail())


@router.get("/image/{post_id}", response_class=FileResponse, summary='Получить изображение:')
async def get_post_image(
    post_id: int,
    DataBase: Session = Depends(get_db),
) -> FileResponse:
    logger.info(f"Запрос изображения для поста id={post_id}")
    use_case = MethodsForImage()
    try:
        result = use_case.get_detail_image(DataBase, post_id)
        logger.info(f"Изображение поста {post_id} отправлено")
        return result
    except PostNotFoundByIDException as e:
        logger.warning(f"Пост id={post_id} для изображения не найден")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail())
    except PostHasNoImageException as e:
        logger.warning(f"Пост id={post_id} не имеет изображения")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail())


@router.post('/', response_model=PostOut,
             status_code=status.HTTP_201_CREATED,
             summary='Создать публикацию:')
def create_post(payload: PostCreateAndUpdate, DataBase: Session = Depends(get_db),
                user: UserOut = Depends(get_current_user)) -> PostOut:
    logger.info(f"Попытка создания поста пользователем {user.nickname}")
    use_case = MethodsForPost()
    try:
        result = use_case.create(DataBase, payload, user.nickname)
        logger.info(f"Пост создан: id={result.id} пользователем {user.nickname}")
        return result
    except PostDontCreateException as e:
        logger.warning(f"Ошибка создания поста пользователем {user.nickname}: {e.get_detail()}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail())


@router.post("/image/{post_id}", status_code=status.HTTP_201_CREATED, response_model=PostImage,
             summary='Прикрепить картинку к публикации:')
async def add_post_image(post_id: int, image: UploadFile = File(...), DataBase: Session = Depends(get_db),
                         user: UserOut = Depends(get_current_user)) -> PostImage:
    logger.info(f"Попытка добавить изображение к посту {post_id} от пользователя {user.nickname}")
    use_case = MethodsForImage()
    try:
        result = use_case.add_image(DataBase, post_id, image, user.nickname)
        logger.info(f"Изображение добавлено к посту {post_id} пользователем {user.nickname}")
        return result
    except PostNotFoundByIDException as e:
        logger.warning(f"Пост {post_id} не найден при добавлении изображения")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail())
    except PostDontChangeException as e:
        logger.warning(f"Пользователь {user.nickname} не может изменить пост {post_id}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=e.get_detail())
    except IsNotAnImageExtensionException as e:
        logger.warning(f"Недопустимое расширение файла: {image.filename}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail())


@router.put('/{post_id}', response_model=PostOut,
            summary='Изменить публикацию:')
def update_post(post_id: int, payload: PostCreateAndUpdate,
                DataBase: Session = Depends(get_db),
                user: UserOut = Depends(get_current_user)) -> PostOut:
    logger.info(f"Попытка обновления поста {post_id} пользователем {user.nickname}")
    use_case = MethodsForPost()
    try:
        result = use_case.update(DataBase, payload, post_id, user.nickname)
        logger.info(f"Пост {post_id} обновлён пользователем {user.nickname}")
        return result
    except PostNotFoundByIDException as e:
        logger.warning(f"Пост {post_id} не найден для обновления")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail())
    except PostDontChangeException as e:
        logger.warning(f"Пользователь {user.nickname} не может изменить пост {post_id}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=e.get_detail())


@router.delete('/{post_id}', status_code=status.HTTP_204_NO_CONTENT,
               summary='Удалить публикацию:')
def delete_post(post_id: int, DataBase: Session = Depends(get_db),
                user: UserOut = Depends(get_current_user)):
    logger.info(f"Попытка удаления поста {post_id} пользователем {user.nickname}")
    use_case = MethodsForPost()
    try:
        use_case.destroy(DataBase, post_id, user.nickname)
        logger.info(f"Пост {post_id} удалён пользователем {user.nickname}")
    except PostNotFoundByIDException as e:
        logger.warning(f"Пост {post_id} не найден для удаления")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail())
    except PostDontDestroyException as e:
        logger.warning(f"Пользователь {user.nickname} не может удалить пост {post_id}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=e.get_detail())


@router.delete('/image/{post_id}', status_code=status.HTTP_204_NO_CONTENT,
               summary='Удалить изображение:')
def delete_image_post(post_id: int, DataBase: Session = Depends(get_db),
                      user: UserOut = Depends(get_current_user)):
    logger.info(f"Попытка удаления изображения поста {post_id} пользователем {user.nickname}")
    use_case = MethodsForImage()
    try:
        use_case.destroy_image(DataBase, post_id, user.nickname)
        logger.info(f"Изображение поста {post_id} удалено пользователем {user.nickname}")
    except PostNotFoundByIDException as e:
        logger.warning(f"Пост {post_id} не найден при удалении изображения")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail())
    except PostDontDestroyException as e:
        logger.warning(f"Пользователь {user.nickname} не может удалить пост {post_id}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=e.get_detail())
    except PostHasNoImageException as e:
        logger.warning(f"Пост {post_id} не имеет изображения для удаления")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.get_detail())
    except ImageDontDestroyException as e:
        logger.warning(f"Пользователь {user.nickname} не может удалить изображение поста {post_id}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=e.get_detail())