import hashlib
from datetime import datetime, timezone

from fastapi import APIRouter, status, HTTPException

from sqlalchemy import select, UUID
from app.database import SessionDep
from app.models.auth import TokenBlacklist
from app.schemas.user import UserCreateSchema, UserResponseSchema, UserLoginSchema, RefreshTokenRequest
from app.models.user import User
from app.security import jwt_password, jwt_utils
from app.services.auth_service import create_token_pair
from fastapi.params import Depends

from app.utils.rate_limiter import rate_limit_ok, rate_limit_login

router = APIRouter()

@router.get("/ok", dependencies=[Depends(rate_limit_ok)])
async def ok_state():
    return "OK"



async def validate_user(
    session: SessionDep,
    login_data: UserLoginSchema,
):
    unauthed_exec = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid email or password",
    )

    res = await session.execute(select(User).where(User.email == login_data.email))
    user = res.scalars().first()

    if not user:
      raise unauthed_exec

    if not jwt_password.validate_pwd(
        password=login_data.password,
        hashed_password=user.password,
    ):
        raise unauthed_exec

    return UserResponseSchema.model_validate(user)


@router.post("/sign_up")
async def sign_up(
    session: SessionDep,
    user_data: UserCreateSchema,
):

    result = await session.execute(select(User).where(User.email == user_data.email))
    existing_email = result.scalars().first()

    if existing_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="email already exists")

    hashed_password = jwt_password.hash_password(user_data.password)

    new_user = User(
        username=user_data.username,
        email=user_data.email,
        password=hashed_password,
    )

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    user_response = UserResponseSchema.model_validate(new_user)

    return create_token_pair(user=user_response)


@router.post("/login", dependencies=[Depends(rate_limit_login)])
async def login(user: UserResponseSchema = Depends(validate_user)):
    return create_token_pair(user)

@router.post("/logout")
async def logout(session: SessionDep,
                 refresh_token_request: RefreshTokenRequest):
    try:
        payload = jwt_utils.decode_jwt(refresh_token_request.refresh_token)
        user_uuid = UUID(payload.get("sub"))
        exp_timestamp = payload.get("exp")

        token_hash = hashlib.sha256(refresh_token_request.refresh_token.encode()).hexdigest()

        blacklisted = await session.execute(select(TokenBlacklist).
                                            where(TokenBlacklist.token_hash == token_hash))

        if not blacklisted:
            jti = payload.get("jti") or token_hash[:64]
            new_blacklist = TokenBlacklist(
                token_id=jti,
                token_hash=token_hash,
                user_uuid=user_uuid,
                expires_at=datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)
            )

            session.add(new_blacklist)
            await session.commit()

            return {"status": "Successfully added to blacklist this token!"}

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Logout failed: {e}")