from pydantic import BaseModel, EmailStr, ConfigDict
from uuid import UUID

class UserCreateSchema(BaseModel):
    username: str
    email: EmailStr | None = None
    password: str


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str


class UserResponseSchema(BaseModel):
    user_uuid: UUID
    username: str
    email: EmailStr | None = None

    model_config = ConfigDict(from_attributes=True)

class RefreshTokenRequest(BaseModel):
    refresh_token: str

class UserCreateResponse(BaseModel):
    email: EmailStr | None = None
    username: str
