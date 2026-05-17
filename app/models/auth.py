from datetime import datetime
from sqlalchemy import String, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base, str_64, str_256, uuid_fk

class TokenBlacklist(Base):
    __tablename__ = "revoked_tokens"

    token_id: Mapped[str_64] = mapped_column(String(64), primary_key=True) #jti
    token_hash: Mapped[str_256] = mapped_column(unique=True, index=True)
    user_uuid: Mapped[uuid_fk] = mapped_column(ForeignKey("user.user_uuid"))
    revoked_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)