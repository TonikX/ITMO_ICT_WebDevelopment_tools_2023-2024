from pydantic import BaseModel, EmailStr

from src.core.pydantic.mixins import SolidUnionMixin

__all__ = ['UserBase']


class UserBase(BaseModel, SolidUnionMixin):
    """Strict readonly"""

    id: int
    email: EmailStr
    hashed_password: str | bytes
    is_active: bool = True
    is_superuser: bool = False
