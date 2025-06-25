from typing import List, Optional
from backend.models import Travel, UserOnTravel
from backend.models import User, UserRole
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, join
from sqlalchemy.orm import joinedload
import asyncio
class UserRepository:

    @staticmethod
    async def get_user(session: AsyncSession, id: int) -> Optional[User]:
        query = select(User).where(User.id == id)
        result = await session.execute(query)
        return result.scalars().first()

    @staticmethod
    async def get_user_by_email(session: AsyncSession, email: str) -> User:
        query = select(User).where(User.email == email)
        result = await session.execute(query)
        return result.scalars().first()

    @staticmethod
    async def get_user_by_login(session: AsyncSession, login: str) -> Optional[User]:
        query = select(User).where(User.login == login)
        result = await session.execute(query)
        return result.scalars().first()

    @staticmethod
    async def create_user(session: AsyncSession, name: str, email: str, password: str, second_name: str, login: str, role: UserRole) -> User:
        user = User(name=name, email=email, password=password, second_name=second_name, role=role, login=login)
        session.add(user)
        return user

    @staticmethod
    async def delete(session: AsyncSession, id: int) -> bool:
        user = await UserRepository.get_user(session, id)
        if not user:
            return False
        await session.delete(user)
        return True

    @staticmethod
    async def update_refresh_token(session: AsyncSession, user_id: int, token: str) -> None:
        user = await UserRepository.get_user(session, user_id)
        user.refresh_token = token

    @staticmethod
    async def get_travels(session: AsyncSession, user_id: int) -> List[Travel]:
        query = select(Travel).join(UserOnTravel, UserOnTravel.travel_id==Travel.id).where(UserOnTravel.user_id == user_id)
        travels = await session.execute(query)
        return list(travels.scalars().all())






