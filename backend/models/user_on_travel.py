from .base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, PrimaryKeyConstraint
from enum import Enum

class Role(Enum):
    CREATER = 'creater'
    USER = 'user'

class UserOnTravel(Base):
    __tablename__ = "user_on_travel"
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    travel_id: Mapped[int] = mapped_column(ForeignKey("travel.id", ondelete="CASCADE"))
    role: Mapped[Role] = mapped_column(nullable=True)
    __table_args__ = (PrimaryKeyConstraint('user_id', 'travel_id'),)