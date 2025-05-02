from typing import Annotated
from sqlalchemy.orm import DeclarativeBase, sessionmaker, mapped_column
from sqlalchemy import create_engine

inpk = Annotated[int, mapped_column(primary_key=True)]

DATABASE_URL = "postgresql+psycopg2://postgres:postgres@localhost:5432/travel_db"
engine = create_engine(
    DATABASE_URL,
    echo=True
)
session_factory = sessionmaker(engine)


class Base(DeclarativeBase):
    pass
