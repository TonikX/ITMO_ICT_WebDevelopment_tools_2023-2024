from datetime import datetime

from pydantic import BaseModel, EmailStr, ConfigDict


class JWT(BaseModel):
    access: str
    refresh: str | None = None

    model_config = ConfigDict(
        frozen=True,
        strict=True,
    )

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
