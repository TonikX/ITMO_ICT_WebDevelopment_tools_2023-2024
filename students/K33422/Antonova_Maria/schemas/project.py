import typing

from pydantic import BaseModel


class ProjectCreate(BaseModel):
    team_id: int
    goal: typing.Optional[str]
    results: typing.Optional[str]


class ProjectUpdate(BaseModel):
    team_id: typing.Optional[int]
    goal: typing.Optional[str]
    results: typing.Optional[str]
