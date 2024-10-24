from typing import TypedDict

from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class UserRead(BaseModel):
    user_id: int
    username: str
    email: str


class UserUpdate(BaseModel):
    username: str
    email: str


class DeletedUserResponse(TypedDict):
    message: str
