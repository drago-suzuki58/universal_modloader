from __future__ import annotations

from pydantic import EmailStr
from sqlmodel import Field, SQLModel

__all__ = [
    "User",
    "UserBase",
    "UserCreate",
    "UserRead",
    "UserUpdate",
    "UserLogin",
    "AuthResponse",
]


class UserBase(SQLModel):
    email: EmailStr = Field(index=True, unique=True)
    full_name: str | None = Field(default=None, max_length=120)
    is_active: bool = Field(default=True)


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str


class UserCreate(UserBase):
    password: str = Field(min_length=8)


class UserRead(UserBase):
    id: int


class UserUpdate(SQLModel):
    email: EmailStr | None = None
    full_name: str | None = Field(default=None, max_length=120)
    password: str | None = Field(default=None, min_length=8)
    is_active: bool | None = None


class UserLogin(SQLModel):
    email: EmailStr
    password: str


class AuthResponse(SQLModel):
    access_token: str
    token_type: str = "bearer"
