from sqlmodel import SQLModel, Field, Relationship
import typing


class SkillsProfiles(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    profile_id: typing.Optional[int] = Field(default=None, foreign_key="profile.id")
    skill_id: typing.Optional[int] = Field(default=None, foreign_key="skill.id")


class SkillsProjects(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    project_id: typing.Optional[int] = Field(default=None, foreign_key="project.id")
    skill_id: typing.Optional[int] = Field(default=None, foreign_key="skill.id")


class Skill(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    description: str = ""
    skills_profiles: typing.Optional[typing.List["Profile"]] = Relationship(
        back_populates="own_skills", link_model=SkillsProfiles
    )
    skills_projects: typing.Optional[typing.List["Project"]] = Relationship(
        back_populates="requirements_skills", link_model=SkillsProjects
    )


class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    username: str
    password: str
    is_active: bool = Field(default=True)
    user_profile: typing.Optional["Profile"] = Relationship(
        back_populates="user", sa_relationship_kwargs={'uselist': False}
    )


class Team(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    description: str
    creator_id: int
    is_active: bool = Field(default=True)
    projects_team: typing.Optional[typing.List["Project"]] = Relationship(back_populates="team_project")
    profiles_team: typing.Optional[typing.List["Profile"]] = Relationship(back_populates="team_profile")


class Project(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    team_id: int = Field(default=None, foreign_key="team.id")
    team_project: Team = Relationship(back_populates="projects_team")
    goal: str
    is_active: bool = Field(default=True)
    requirements_skills: typing.Optional[typing.List[Skill]] = Relationship(
        back_populates="skills_projects", link_model=SkillsProjects
    )
    results: str


class Profile(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: typing.Optional[int] = Field(default=None, foreign_key="user.id")
    user: typing.Optional[User] = Relationship(back_populates="user_profile")
    is_active: bool = Field(default=True)
    description: typing.Optional[str]
    team_id: typing.Optional[int] = Field(default=None, foreign_key="team.id")
    team_profile: typing.Optional[Team] = Relationship(back_populates="profiles_team")
    own_skills: typing.Optional[typing.List[Skill]] = Relationship(
        back_populates="skills_profiles", link_model=SkillsProfiles,
        sa_relationship_kwargs={'uselist': True}
    )
    projects_interests: typing.Optional[str]
    experience: typing.Optional[str]


class Page(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    url: str
    title: str
