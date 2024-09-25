import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, ValidationInfo, field_validator
from sqlmodel import SQLModel, Field, Relationship

from ..models.auth import Token


class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    username: str = Field(index=True)
    password: str = Field(min_length=4, max_length=64)
    email: str = Field(...)
    balance: Optional["Balance"] = Relationship(back_populates="user")  # type: ignore  # noqa: F821
    created_at: datetime.datetime = Field(default=datetime.datetime.now())


class UserInput(BaseModel):
    username: str = Field(...)
    password: str = Field(min_length=4, max_length=64)
    password_confirm: str = Field(min_length=4, max_length=64)
    email: EmailStr

    @field_validator("password_confirm")
    @classmethod
    def check_password_match(cls, v, info: ValidationInfo):
        if "password" in info.data and v != info.data["password"]:
            raise ValueError("Passwords do not match")
        return v


class UserLogin(BaseModel):
    username: str = Field(...)
    password: str = Field(...)


class UserChangePassword(BaseModel):
    password: str = Field(min_length=4, max_length=64)
    password_confirm: str = Field(min_length=4, max_length=64)

    @field_validator("password_confirm")
    @classmethod
    def check_password_match(cls, v, info: ValidationInfo):
        if "password" in info.data and v != info.data["password"]:
            raise ValueError("Passwords do not match")
        return v


class UserRegisterResponse(BaseModel):
    id: int = Field(...)
    username: str = Field(...)
    email: str = Field(...)
    created_at: datetime.datetime = Field(...)
    token: Token = Field(...)


class UserMeResponse(BaseModel):
    id: int = Field(...)
    username: str = Field(...)
    email: str = Field(...)
    created_at: datetime.datetime = Field(...)
