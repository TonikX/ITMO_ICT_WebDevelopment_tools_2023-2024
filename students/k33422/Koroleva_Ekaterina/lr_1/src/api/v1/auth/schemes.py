from pydantic import BaseModel, EmailStr

from src.core.pydantic.mixins import SolidMixin


class UserCredentials(BaseModel, SolidMixin):
    email: EmailStr
    password: str


class UserPrivate(BaseModel, SolidMixin):
    email: EmailStr


class PasswordChange(BaseModel, SolidMixin):
    old_password: str
    new_password: str
