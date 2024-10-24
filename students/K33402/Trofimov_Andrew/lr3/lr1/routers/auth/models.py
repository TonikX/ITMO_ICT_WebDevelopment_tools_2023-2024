from typing import TypedDict

from pydantic import BaseModel


class TokenCreate(BaseModel):
    email: str
    password: str


class TokenCreateResponse(TypedDict):
    token: str
