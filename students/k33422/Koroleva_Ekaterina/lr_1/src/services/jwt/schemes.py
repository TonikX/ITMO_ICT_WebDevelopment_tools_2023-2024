from datetime import datetime

from pydantic import BaseModel, EmailStr

from src.core.pydantic.mixins import SolidMixin, UnionMixin

__all__ = ['JWT', 'Payload']


class JWT(BaseModel, SolidMixin):
    access: str
    refresh: str | None = None

    def __str__(self):
        return f'Bearer {self.access}'


class Payload(BaseModel, UnionMixin):
    sub: str
    exp: datetime
    iat: datetime

    email: EmailStr
    is_superuser: bool = False
