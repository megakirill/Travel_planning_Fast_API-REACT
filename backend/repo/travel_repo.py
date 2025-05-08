from typing import Optional

from sqlalchemy.orm import joinedload, selectinload

from backend.models import Travel, UserOnTravel, travel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, join

class TravelRepository:
    @staticmethod
    async def get_travel(session: AsyncSession, travel_id: int) -> Travel:
        query = select(Travel).options(selectinload(Travel.cards)).where(Travel.id == travel_id)
        travel = await session.execute(query)
        return travel.scalar_one_or_none()

    @staticmethod
    async def get_all(session: AsyncSession) -> list[Travel]:
        query = select(Travel).options(selectinload(Travel.cards))
        travels = await session.execute(query)
        return travels.scalars().all()

    @staticmethod
    async def create_travel(session: AsyncSession, name: str, description: str) -> Travel:
        travel = Travel.create(name=name, description=description)
        session.add(travel)
        return travel

    @staticmethod
    async def update_travel(session: AsyncSession, travel_id: int, name: str, description: str) -> Travel:
        pass

    @staticmethod
    async def delete_travel(session: AsyncSession, travel_id: int) -> bool:
        travel = await TravelRepository.get_travel(session, travel_id)
        if not travel:
            return False
        await session.delete(travel)
        return True

    @staticmethod
    async def get_travels_by_user(session: AsyncSession, user_id: int) -> Optional[list[Travel]|None]:
        query = select(Travel).join(UserOnTravel, Travel.id == UserOnTravel.travel_id).options(selectinload(Travel.cards)).where(UserOnTravel.user_id == user_id)
        travels = await session.execute(query)
        travels = travels.scalars().all()
        return travels if travels else None

    @staticmethod
    async def add_user_to_travel(session: AsyncSession, travel_id: int, user_id: int, role: str):
        a = UserOnTravel(travel_id=travel_id, user_id=user_id, role=role)
        session.add(a)

    @staticmethod
    async def remove_user_from_travel(session: AsyncSession, travel_id: int, user_id: int):
        query = select(UserOnTravel).where((UserOnTravel.travel_id == travel_id) & (UserOnTravel.user_id == user_id))
        user = await session.execute(query)
        await session.delete(user)

    @staticmethod
    async def get_users_in_travel(session: AsyncSession, travel_id: int) -> Optional[list[UserOnTravel]|None]:
        query = select(Travel).options(selectinload(Travel.users)).where(Travel.id == travel_id)
        travel = await session.execute(query)
        travel = travel.scalar_one_or_none()
        return travel.users if travel else None

    @staticmethod
    async def get_user_role_in_travel(session: AsyncSession, travel_id: int, user_id: int):
        query = select(UserOnTravel.role).where((UserOnTravel.travel_id == travel_id) & (UserOnTravel.user_id == user_id))
        user = await session.execute(query)
        return user.scalar_one_or_none()


