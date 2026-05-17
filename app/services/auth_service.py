from datetime import datetime
import uuid
from datetime import UTC, timedelta

from app.schemas.auth import TokenResponseSchema
from app.schemas.user import UserResponseSchema
from app.config import settings
from app.security import jwt_utils


TOKEN_TYPE_FIELD = "type"
_ACCESS_TOKEN = "access"
_REFRESH_TOKEN = "refresh"

def create_token(
    token_type: str,
    token_data: dict,
    expire_minutes: int = 0,
    expire_timedelta: timedelta | None = None
):
    jwt_payload = {TOKEN_TYPE_FIELD: token_type}
    jwt_payload.update(token_data)
    return jwt_utils.encode_jwt(
        payload=jwt_payload,
        expire_minutes=expire_minutes,
        expire_timedelta=expire_timedelta,
    )

def create_access_token(user: UserResponseSchema) -> str:
    jti = str(uuid.uuid4())
    jwt_payload = {
        "sub": str(user.user_uuid),
        "email": user.email,
        "jti": jti,
        "iat": datetime.now(UTC),
    }

    return create_token(
        token_type=_ACCESS_TOKEN,
        token_data=jwt_payload,
        expire_minutes = settings.auth_jwt.access_token_expire_minutes
    )



def create_refresh_token(user: UserResponseSchema) -> str :
    jti = str(uuid.uuid4())
    jwt_payload = {
        "sub": str(user.user_uuid),
        "email": user.email,
        "jti": jti,
        "iat": datetime.now(UTC),
    }

    return create_token(
        token_type=_REFRESH_TOKEN,
        token_data=jwt_payload,
        expire_timedelta=timedelta(days=settings.auth_jwt.refresh_token_expire_days)
    )

def create_token_pair(user: UserResponseSchema):
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)
    return TokenResponseSchema(
        access_token=access_token,
        refresh_token=refresh_token,
        user_data=user.model_dump()
    )