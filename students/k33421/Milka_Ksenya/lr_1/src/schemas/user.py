import typing as tp

from pydantic import BaseModel, ConfigDict

from .project import Project
from .skill import UserSkill


class UserCRUD(BaseModel):
    first_name: tp.Optional[str]
    last_name: tp.Optional[str]
    email: tp.Optional[str]
    about: tp.Optional[str]


class User(UserCRUD):
    id: int
    username: str

    model_config = ConfigDict(from_attributes=True)


class UserMe(User):
    created_projects: list[Project]
    skills: list[UserSkill]


class UserMember(User):
    role: str
