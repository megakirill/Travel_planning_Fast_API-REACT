from .base import Base, inpk
from sqlalchemy.orm import Mapped, mapped_column, relationship
from enum import Enum

class UserRole(Enum):
    user = 'user'
    admin = 'admin'
    editor = 'editor'


class User(Base):
    __tablename__ = "users"

    id: Mapped[inpk]
    login: Mapped[str]
    name: Mapped[str]
    second_name: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    travels: Mapped[list["Travel"]] = relationship(back_populates='users', secondary='user_on_travel')
    role: Mapped[UserRole] = mapped_column(nullable=True)

    def __repr__(self):
        return f'<id: {self.id}, name: {self.name} {self.second_name}, email: {self.email}'