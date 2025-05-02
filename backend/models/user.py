from .base import Base, inpk
from sqlalchemy.orm import Mapped, mapped_column, relationship

class User(Base):
    __tablename__ = "user"

    id: Mapped[inpk]
    name: Mapped[str]
    second_name: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    refresh_token: Mapped[str]
    travels: Mapped["Travel"] = relationship(back_populates='users', secondary='user_on_travel')

    def __repr__(self):
        return f'<id: {self.id}, name: {self.name} {self.second_name}, email: {self.email}, refresh_token: {self.refresh_token}'