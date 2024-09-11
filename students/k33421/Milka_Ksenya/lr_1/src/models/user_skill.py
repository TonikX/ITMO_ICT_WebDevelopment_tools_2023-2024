import typing as tp

from sqlmodel import Field, Relationship, SQLModel

if tp.TYPE_CHECKING:
    from .skill import Skill
    from .user import User


class UserSkill(SQLModel, table=True):
    user_id: tp.Optional[int] = Field(None, foreign_key="user.id", primary_key=True)
    skill_id: tp.Optional[int] = Field(None, foreign_key="skill.id", primary_key=True)
    level: int = 1

    user: "User" = Relationship(back_populates="user_skills")
    skill: "Skill" = Relationship(back_populates="user_skills")
