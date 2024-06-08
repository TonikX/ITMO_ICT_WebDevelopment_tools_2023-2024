from __future__ import annotations

from datetime import date

from pydantic import BaseModel


class TripBase(BaseModel):
    title: str
    description: str | None = None
    region_id: int
    place_id: int | None = None
    start_date: date | None = None
    expected_end_date: date | None = None


class TripCreate(TripBase):
    pass


class TripPlanned(TripBase):
    id: int
    initiator_id: int
    companion_id: int | None

    class Config:
        orm_mode = True


class TripCompleted(TripBase):
    id: int
    initiator_id: int
    companion_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str


class UserInfo(UserBase):
    personal_information: str | None
    travelling_skills: str | None
    personal_transport: str | None
    companion_preferences: str | None


class UserCreate(UserInfo):
    password: str


class UserOutFull(UserInfo):
    id: int
    is_active: bool
    planned_trips: list[TripPlanned]
    completed_trips: list[TripCompleted]

    class Config:
        orm_mode = True


class UserOutBrief(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True
