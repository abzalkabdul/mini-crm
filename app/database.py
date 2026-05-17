import uuid
from typing import Annotated

from fastapi.params import Depends
from sqlalchemy import String, UUID
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, mapped_column

import uuid as uuid_lib
from app.config import settings

engine = create_async_engine(
    url=settings.db_url,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
)

async_session_factory = async_sessionmaker(
    engine,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)

async def get_db():
    async with async_session_factory() as session:
        yield session


str_64 = Annotated[str, 64]
str_256 = Annotated[str, 256]
str_50 = Annotated[str, 50]

class Base(DeclarativeBase):
    __abstract__ = True

    type_annotation_map = {
        str_64: String(64),
        str_256: String(256),
        str_50: String(50),
    }


SessionDep = Annotated[AsyncSession, Depends(get_db)]

uuid_pk = Annotated[uuid_lib.UUID,
                    mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())]

uuid_fk = Annotated[uuid_lib.UUID,
                    mapped_column(UUID(as_uuid=True))]