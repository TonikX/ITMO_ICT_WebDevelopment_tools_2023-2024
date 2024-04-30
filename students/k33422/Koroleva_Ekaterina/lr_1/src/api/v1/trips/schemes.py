from datetime import date

from pydantic import BaseModel, EmailStr

from src.core.pydantic.mixins import SolidMixin, SolidUnionMixin
from src.models import Gender


class UserSingle(BaseModel, SolidUnionMixin):
    id: int
    email: EmailStr


class ProfileSingle(BaseModel, SolidUnionMixin):
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
    user: UserSingle


class ParticipantMulti(BaseModel, SolidUnionMixin):
    id: int
    user_id: int
    first_name: str
    last_name: str
    middle_name: str
    birth_date: date
    gender: Gender
    bio: str = ''
    country: str
    city: str | None
    language: str


class TripMulti(BaseModel, SolidUnionMixin):
    id: int
    title: str
    description: str
    start_date: date
    end_date: date
    start_location: str
    destination: str
    profile: ProfileSingle


class MyTripMulti(BaseModel, SolidUnionMixin):
    id: int
    title: str
    description: str
    start_date: date
    end_date: date
    start_location: str
    destination: str


class TripSingle(BaseModel, SolidUnionMixin):
    id: int
    title: str
    description: str
    start_date: date
    end_date: date
    start_location: str
    destination: str
    profile: ProfileSingle
    participants: list[ParticipantMulti]


class MyTripSingle(BaseModel, SolidUnionMixin):
    id: int
    title: str
    description: str
    start_date: date
    end_date: date
    start_location: str
    destination: str
    participants: list[ParticipantMulti]


class MyTripSingleAfterOperation(BaseModel, SolidUnionMixin):
    id: int
    title: str
    description: str
    start_date: date
    end_date: date
    start_location: str
    destination: str


class CreateMyTrip(BaseModel, SolidMixin):
    title: str
    description: str = ''
    start_date: date
    end_date: date
    start_location: str
    destination: str


class UpdateMyTrip(BaseModel, SolidMixin):
    title: str
    description: str
    start_date: date
    end_date: date
    start_location: str
    destination: str


class PartialUpdateMyTrip(BaseModel, SolidMixin):
    title: str | None = None
    description: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    start_location: str | None = None
    destination: str | None = None
