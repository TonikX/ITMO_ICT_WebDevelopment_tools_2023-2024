import typing as tp

from sqlmodel import Relationship, SQLModel

from . import mixins

if tp.TYPE_CHECKING:
    from .user_skill import UserSkill


class Skill(mixins.IDMixin, SQLModel, table=True):
    name: str
    description: tp.Optional[str] = None

    user_skills: list["UserSkill"] = Relationship(back_populates="skill")
