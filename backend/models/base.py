from typing import Annotated
from sqlalchemy.orm import DeclarativeBase, sessionmaker, mapped_column
from sqlalchemy import create_engine
import os


inpk = Annotated[int, mapped_column(primary_key=True)]

DATABASE_URL = os.environ.get('DATABASE_URL')
engine = create_engine(
    DATABASE_URL,
    echo=True
)
session_factory = sessionmaker(engine)


class Base(DeclarativeBase):
    pass
