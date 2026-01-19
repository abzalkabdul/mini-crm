from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import String

from config import settings


async_engine = create_async_engine(
    url=settings.DB_URL_asyncpg,
    echo=True,
)

async_session_factory = async_sessionmaker(async_engine, expire_on_commit=False)

async def get_session():
    async with async_session_factory() as session:
        yield session

SessionDep = Annotated[AsyncSession, Depends(get_session)]

str_256 = Annotated[String, 256]

class Base(DeclarativeBase):
    type_annotation_map = {
        str_256: String(256)
    }
    
    __table_args__ = {
        ...
    }