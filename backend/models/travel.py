from .base import Base, inpk
from sqlalchemy.orm import Mapped, mapped_column, relationship

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


