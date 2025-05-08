from .base import Base, inpk
from sqlalchemy.orm import Mapped, mapped_column, relationship
import uuid
import os

DOMEN = os.environ.get("DOMEN")

class Travel(Base):
    __tablename__ = "travel"

    id: Mapped[inpk]
    name: Mapped[str] = mapped_column(nullable=True)
    description: Mapped[str]
    link: Mapped[str]
    code: Mapped[str] = mapped_column(unique=True)
    cards: Mapped["Card"] = relationship(back_populates="travel")
    users: Mapped["User"] = relationship(back_populates='travels',
                                         secondary='user_on_travel')

    @classmethod
    def create(cls, name:str, description:str):
        return cls(name=name, description=description,
                   link=f'htts://{DOMEN}/{uuid.uuid4().hex[:10]}',
                   code=uuid.uuid4().hex[:6].upper())

