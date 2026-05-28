from datetime import datetime
from typing import Optional

from sqlalchemy import Text, DateTime, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped
from app.database import Base, uuid_fk, uuid_pk, str_50


class Task(Base):
    __tablename__ = "tasks"

    task_uuid: Mapped[uuid_pk]
    title: Mapped[str_50] = mapped_column(Text, unique=True)
    description: Mapped[Optional[str]] = mapped_column(nullable=True)
    deadline: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    appointed: Mapped[uuid_fk] = mapped_column(ForeignKey("users.user_uuid"))
    deal: Mapped[uuid_fk] = mapped_column(ForeignKey("deals.deal_uuid"))
