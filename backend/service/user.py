from typing import Annotated, Optional
from fastapi import HTTPException
from httpx import Auth
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext
from backend.models import AsyncSessionFactory, User
from backend.repo import UserRepository
from backend.schemas.user import UserCreate, UserRead, UserUpdate
from backend.schemas.auth import UserLogin
from .auth import AuthService
from backend.schemas.auth import UserForToken
from backend.service.auth import AuthService


class UserService:
    @staticmethod
    async def create_user(user: UserCreate):
        async with AsyncSessionFactory() as session:
            try:
                a = await UserRepository.get_user_by_email(session, user.email)
                if not a:
                    print('начал')
                    hashed_password = AuthService.create_hash_password(user.password)
                    print('закончил')
                    print(hashed_password)
                    new_user = await UserRepository.create_user(
                        session=session,
                        login=user.login,
                        email=user.email,
                        password=hashed_password,
                        name=user.name,
                        second_name=user.second_name,
                        role='user'
                    )
                    await session.flush()
                    await session.refresh(new_user)
                    new_user = UserRead.model_validate(new_user)

                    await session.commit()
                    return new_user
                print('наход')
                await session.rollback()
                return None
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    async def get_user_by_id(id: int) -> Optional[UserRead]:
        async with AsyncSessionFactory() as session:
            a = await UserRepository.get_user(session, id)
            await session.commit()
            if a:
                return UserRead.model_validate(a, from_attributes=True)
            return None


    @staticmethod
    async def get_user_by_email(email: str) -> UserRead:
        async with AsyncSessionFactory() as session:
            a = await UserRepository.get_user_by_email(session, email)
            await session.commit()
            return UserRead.model_validate(a)

    @staticmethod
    async def delete_user(id: int) -> bool:
        async with AsyncSessionFactory() as session:
            a = await UserRepository.delete(session, id)
            await session.commit()
            return a

    @staticmethod
    async def update_user(session: AsyncSession, user: User, user_new: UserUpdate) -> UserRead:
        for key, value in user_new.model_dump().items():
            setattr(user, key, value)
        await session.commit()
        await session.refresh(user)
        return UserRead.model_validate(user, from_attributes=True)

    @staticmethod
    async def login_user(session: AsyncSession, user: UserLogin) -> UserForToken:
        a = await UserRepository.get_user_by_login(session, user.login)
        await session.commit()
        if not a:
            raise HTTPException(status_code=404, detail="User not found")
        b = UserForToken.model_validate(a)
        if AuthService.verify_password(user.password,b.password):
            return b
        else:
            raise HTTPException(status_code=401, detail="Wrong password")






