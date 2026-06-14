import os
from uuid import uuid4
import shutil
from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import File
from fastapi.responses import FileResponse

from src.infrastructure.postgre.repositories.posts import PostRepository
from src.infrastructure.postgre.models.post_models import PostModel
from src.core.exceptions.database_exceptions import CredentialException, PostNotFoundException
from src.schems.posts import PostImage
from src.core.exceptions.domain_exceptions import ImageDontDestroyException, IsNotAnImageExtensionException, PostDontChangeException, PostHasNoImageException, PostNotFoundByIDException


class MethodsForImage:
    def __init__(self):
        self._repo = PostRepository()

    async def add_image(self, DataBase: AsyncSession, post_id: int, image: File,
                  nickname: str, image_folder = "images") -> PostImage:
        extension = image.filename.split(".")[-1]
        if extension not in ['jpeg', 'jpg', 'png']:
            raise IsNotAnImageExtensionException(extension)
        
        try:
            post_model = await self._repo.get_detail(DataBase, post_id)
            if post_model.image:
                await self._repo.update_image(DataBase, post_model.image, post_id, nickname)
                image_path = f"{image_folder}/{post_model.image}"
                os.remove(image_path)
            else:
                new_image_name: str = str(uuid4())
                new_image_name_and_extension: str = f"{new_image_name}.{extension}"
                await self._repo.update_image(DataBase, new_image_name_and_extension, post_id, nickname)
                image_path = f"{image_folder}/{new_image_name_and_extension}"
            with open(image_path, "wb") as buffer:
                shutil.copyfileobj(image.file, buffer)
        except PostNotFoundException:
            raise PostNotFoundByIDException(post_id)
        except CredentialException:
            raise PostDontChangeException('данный пост не принадлежит этому пользователю')
        

        return PostImage(image=image_path)
    
    async def get_detail_image(self, DataBase: AsyncSession, post_id: int, image_folder = "images") -> FileResponse:
        try:
            post_model = await self._repo.get_detail(DataBase, post_id)
        except PostNotFoundException:
            raise PostNotFoundByIDException(post_id)

        if not post_model.image:
            raise PostHasNoImageException()
        extension = post_model.image.split('.')[-1]
        full_image_path: str = f"{image_folder}/{post_model.image}"
        return FileResponse(full_image_path, media_type=f"image/{extension}")
    
    async def destroy_image(self, DataBase: AsyncSession, post_id: int, nickname: str, image_folder: str = "images") -> None:
        try:
            post = await self._repo.get_detail(DataBase, post_id)
            image = str(post.image)
            if image:
                await self._repo.update_image(DataBase, "", post_id, nickname)
                image_path = f"{image_folder}/{image}"
                os.remove(image_path)
            else: raise PostHasNoImageException()
        except PostNotFoundException:
            raise PostNotFoundByIDException(post_id)
        except CredentialException:
            raise ImageDontDestroyException('пост данного изображения не принадлежит этому пользователю')
    
@event.listens_for(PostModel, 'after_delete')
def destroy_image_after_destroy_post(mapper, connection, target) -> None:
    image_folder: str = "images"
    image = str(target.image)
    if image:
        image_path = f"{image_folder}/{image}"
        os.remove(image_path)
