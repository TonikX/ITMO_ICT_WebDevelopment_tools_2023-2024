import typing

from pydantic import BaseModel, Extra


class TeamUpdate(BaseModel):
    name: typing.Optional[str]


class TeamCreate(BaseModel, extra=Extra.allow):
    name: str
    description: typing.Optional[str]


class TeamParticipantUpdate(BaseModel):
    team_id: int
    profile_id: int
