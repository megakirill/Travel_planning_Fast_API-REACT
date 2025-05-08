from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models import Card

class CardRepository:
    @staticmethod
    async def get_card(session: AsyncSession, id: int) -> Card:
        query = select(Card).where(Card.id == id)
        card = await session.execute(query)
        return card.scalars().all()

    @staticmethod
    async def create_card(session: AsyncSession, travel_id: int, city: str, description: str, user_id: int) -> Card:
        card = Card(id_travel=travel_id, city=city, description=description, id_last_change=user_id)
        session.add(card)
        return card

    @staticmethod
    async def delete(session: AsyncSession, id: int) -> bool:
        card = await CardRepository.get_card(session, id)
        if not card:
            return False
        await session.delete(card)
        return True
