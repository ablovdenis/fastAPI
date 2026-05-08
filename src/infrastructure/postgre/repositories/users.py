from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from ..models.user_models import UserModel
from ....schems.users import UserCreate, UserUpdate
from src.core.exceptions.database_exceptions import (UserNotFoundException,
                                                     UserByNicknameAlreadyExistsException,
                                                     UserByEmailAlreadyExistsException)


class UserRepository:
    def __init__(self):
        pass

    async def get(self, db: AsyncSession, skip: int, limit: int) -> List[UserModel]:
        stmt = select(UserModel).offset(skip).limit(limit)
        result = await db.execute(stmt)
        return result.scalars().all()

    async def get_detail(self, db: AsyncSession, nickname: str) -> UserModel:
        stmt = select(UserModel).where(UserModel.nickname == nickname)
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()
        if not user:
            raise UserNotFoundException()
        return user

    async def create(self, db: AsyncSession, payload: UserCreate) -> UserModel:
        user = UserModel(**payload.model_dump())
        db.add(user)
        try:
            await db.commit()
        except IntegrityError as e:
            str_error = str(e.orig)
            if 'nickname' in str_error:
                raise UserByNicknameAlreadyExistsException()
            elif 'email' in str_error:
                raise UserByEmailAlreadyExistsException()
            else:
                raise IntegrityError
        await db.refresh(user)
        return user

    async def update(self, db: AsyncSession, nickname: str, payload: UserUpdate) -> UserModel:
        user = await self.get_detail(db, nickname)
        update_data = payload.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user, field, value)
        try:
            await db.commit()
        except IntegrityError:
            raise UserByEmailAlreadyExistsException()
        await db.refresh(user)
        return user

    async def destroy(self, db: AsyncSession, nickname: str) -> None:
        user = await self.get_detail(db, nickname)
        await db.delete(user)
        await db.commit()