import typing as tp

from pydantic import BaseModel


class Skill(BaseModel):
    id: int
    name: str
    description: tp.Optional[str]


class UserSkill(Skill):
    level: int
