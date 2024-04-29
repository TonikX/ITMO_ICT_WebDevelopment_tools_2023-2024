from datetime import datetime

from pydantic import BaseModel, EmailStr, ConfigDict

from src.core.pydantic.mixins import SolidMixin

__all__ = ['JWT', 'Payload']


class JWT(BaseModel, SolidMixin):
    access: str
    refresh: str | None = None

    def __str__(self):
        return f'Bearer {self.access}'


class Payload(BaseModel):
    sub: str
    exp: datetime
    iat: datetime

    email: EmailStr
    is_superuser: bool = False

    model_config = ConfigDict(
        from_attributes=True
    )
