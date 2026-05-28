from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base, uuid_pk, str_50, str_64

class Contact(Base):
    __tablename__ = "contacts"

    contact_uuid: Mapped[uuid_pk]
    name: Mapped[str_50]
    email: Mapped[Optional[str]] = mapped_column(unique=True, nullable=True)
    company: Mapped[str_64]