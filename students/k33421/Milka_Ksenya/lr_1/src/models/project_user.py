import typing as tp

from sqlmodel import Field, Relationship, SQLModel

if tp.TYPE_CHECKING:
    from .project import Project
    from .user import User


class ProjectUser(SQLModel, table=True):
    project_id: tp.Optional[int] = Field(None, foreign_key="project.id", primary_key=True)
    user_id: tp.Optional[int] = Field(None, foreign_key="user.id", primary_key=True)
    role: str

    project: "Project" = Relationship(back_populates="members")
    user: "User" = Relationship(back_populates="members")
