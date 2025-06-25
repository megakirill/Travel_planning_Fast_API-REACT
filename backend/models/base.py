from typing import Annotated, Any, AsyncGenerator, Optional
from sqlalchemy.orm import DeclarativeBase, sessionmaker, mapped_column
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
import os


inpk = Annotated[int, mapped_column(primary_key=True)]

DATABASE_URL = os.environ.get('DATABASE_URL')
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")
engine = create_async_engine(
    DATABASE_URL,
    echo=True
)
AsyncSessionFactory = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,  # Отключаем автоматический expire после commit
    class_=AsyncSession
)



class Base(DeclarativeBase):
    pass

async def get_session() -> AsyncGenerator[Optional[AsyncSession], Any]:
    async with AsyncSessionFactory() as session:
        yield session

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

