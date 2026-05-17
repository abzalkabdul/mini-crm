from typing import Optional
from datetime import datetime
from sqlalchemy import DateTime, func, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base, uuid_pk

class User(Base):
    __tablename__ = "users"

    user_uuid: Mapped[uuid_pk]
    username: Mapped[str]
    email: Mapped[Optional[str]] = mapped_column(unique=True, nullable=True)
    password: Mapped[str]
    public_key: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now())
    last_login: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
