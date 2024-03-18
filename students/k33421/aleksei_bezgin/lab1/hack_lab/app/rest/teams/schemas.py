import datetime

from sqlmodel import SQLModel


class MemberBase(SQLModel):
    id: int
    role: str


class Member(MemberBase):
    username: str
    full_name: str | None = None
    email: str | None
    contact_number: str | None = None


class Hackathon(SQLModel):
    id: int
    name: str
    start_date: datetime.datetime
    end_date: datetime.datetime


class Team(SQLModel):
    id: int
    name: str

    hackathon: Hackathon
    members: list[Member] | None = None


class TeamCreateData(SQLModel):
    name: str
    hackathon_id: int
    members: list[MemberBase] | None = None


class TeamUpdateData(SQLModel):
    name: str | None = None
    hackathon_id: int | None = None