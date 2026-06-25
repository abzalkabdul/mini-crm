from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base, uuid_fk, uuid_pk,str_50
from app.models.enum import Status


class Deal(Base):
    __tablename__ = "deals"

    deal_uuid: Mapped[uuid_pk]
    name: Mapped[str_50]
    amount: Mapped[int]
    status: Mapped[Status]
    contact_uuid: Mapped[uuid_fk] = mapped_column(ForeignKey("contacts.contact_uuid"))
    owner_uuid: Mapped[uuid_fk] = mapped_column(ForeignKey("users.user_uuid"))
