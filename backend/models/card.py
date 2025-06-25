from .base import Base, inpk
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey
from datetime import datetime

class Card(Base):
    __tablename__ = "card"

    id: Mapped[inpk]
    id_travel: Mapped[int] = mapped_column(ForeignKey('travel.id', ondelete="CASCADE"))
    city: Mapped[str] = mapped_column(unique=True, nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    id_last_change: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=True)
    data_change: Mapped[datetime] = mapped_column(onupdate=datetime.utcnow, default=datetime.utcnow)
    travel: Mapped["Travel"] = relationship(back_populates="cards")

    def update_id_last_change(self, id: int):
        self.id_last_change = id