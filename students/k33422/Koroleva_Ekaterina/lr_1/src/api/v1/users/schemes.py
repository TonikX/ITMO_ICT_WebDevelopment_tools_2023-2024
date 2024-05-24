from datetime import date

from pydantic import BaseModel, EmailStr

from src.core.pydantic.mixins import SolidMixin, SolidUnionMixin
from src.models import Gender


class ProfileMe(BaseModel, SolidUnionMixin):
    id: int
    first_name: str
    last_name: str
    middle_name: str
    birth_date: date
    gender: Gender
    bio: str = ''
    country: str
    city: str | None
    language: str


class ProfileCreate(BaseModel, SolidMixin):
    first_name: str
    last_name: str
    middle_name: str
    birth_date: date
    gender: Gender
    bio: str = ''
    country: str
    city: str | None = None
    language: str


class ProfileUpdate(BaseModel, SolidMixin):
    first_name: str
    last_name: str
    middle_name: str
    birth_date: date
    gender: Gender
    bio: str
    country: str
    city: str | None
    language: str


class ProfilePartialUpdate(BaseModel, SolidMixin):
    first_name: str | None = None
    last_name: str | None = None
    middle_name: str | None = None
    birth_date: date | None = None
    gender: Gender | None = None
    bio: str | None = None
    country: str | None = None
    city: str | None = None
    language: str | None = None


class UserMe(BaseModel, SolidUnionMixin):
    id: int
    email: EmailStr
    profile: ProfileMe | None


class UserMultiPublic(BaseModel, SolidUnionMixin):
    id: int
    email: EmailStr


class UserSinglePublic(BaseModel, SolidUnionMixin):
    id: int
    email: EmailStr
    profile: ProfileMe | None
