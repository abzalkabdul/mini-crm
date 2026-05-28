from fastapi import APIRouter, Depends
from sqlalchemy import select, update, delete
from fastapi.security import HTTPBearer

from uuid import UUID

from app.auth.router import http_bearer
from app.database import SessionDep
from app.models.user import User
from app.schemas.user import UserCreateSchema, UserCreateResponse

router = APIRouter(prefix="/users",
                   tags=["RBD"],
                   dependencies=[Depends(http_bearer)],
                   )

@router.get("/")
async def get_users(session: SessionDep):
    query = await session.execute(select(User))
    users = query.scalars().all()
    return users

@router.get("/{id}")
async def get_user(user_uuid: UUID, session: SessionDep):
    result = await session.execute(select(User).where(User.user_uuid == user_uuid))
    user = result.scalars().first()
    return user

@router.post("/new_user")
async def create_user(session: SessionDep,
                      user_data: UserCreateSchema) -> UserCreateResponse:

    new_user = User(**user_data.model_dump())
    session.add(new_user)
    await session.commit()

    return UserCreateResponse(username=user_data.username,
                              email=user_data.email)

@router.patch("/update_username")
async def update_user(user_uuid: UUID, username: str, session: SessionDep):
    await session.execute(update(User)
                          .where(User.user_uuid == user_uuid)
                          .values(username=username))

    await session.commit()
    return {"status": "success"}


@router.delete("/{id}")
async def delete_user(user_uuid: UUID, session: SessionDep):
    await session.execute(delete(User).where(User.user_uuid == user_uuid))
    await session.commit()
    return {"status": "success"}
