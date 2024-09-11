from datetime import datetime

from pydantic import BaseModel


class Payload(BaseModel):
    sub: int
    exp: datetime
    iat: datetime


class AccessToken(BaseModel):
    access_token: str


class Sign(BaseModel):
    username: str
    password: str


class ChangePassword(BaseModel):
    old_password: str
    new_password: str
