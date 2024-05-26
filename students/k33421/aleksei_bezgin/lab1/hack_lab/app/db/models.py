import datetime

from sqlmodel import SQLModel, Field, Relationship


class MemberTeamLink(SQLModel, table=True):
    __tablename__ = "member_team_links"

    team_id: int | None = Field(default=None, foreign_key="teams.id", primary_key=True)
    member_id: int | None = Field(default=None, foreign_key="users.id", primary_key=True)
    role: str

    team: "Team" = Relationship(back_populates="member_links")
    member: "User" = Relationship(back_populates="team_links")


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: int | None = Field(default=None, primary_key=True)

    username: str
    hashed_password: str
    full_name: str | None = None
    email: str | None
    contact_number: str | None

    team_links: list[MemberTeamLink] | None = Relationship(
        back_populates="member",
        sa_relationship_kwargs={
            "cascade": "all, delete",
        },
    )


class Team(SQLModel, table=True):
    __tablename__ = "teams"

    id: int | None = Field(default=None, primary_key=True)

    name: str
    hackathon_id: int = Field(foreign_key="hackathons.id")

    hackathon: "Hackathon" = Relationship(back_populates="teams")
    member_links: list[MemberTeamLink] = Relationship(
        back_populates="team",
        sa_relationship_kwargs={
            "cascade": "all, delete",
        },
    )
    submissions: list["Submission"] = Relationship(
        back_populates="team",
        sa_relationship_kwargs={
            "cascade": "all, delete",
        },
    )


class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: int | None = Field(default=None, primary_key=True)

    title: str
    description: str
    requirements: str
    evaluation_criteria: str
    hackathon_id: int = Field(foreign_key="hackathons.id")

    hackathon: "Hackathon" = Relationship(back_populates="tasks")
    submissions: list["Submission"] = Relationship(
        back_populates="task",
        sa_relationship_kwargs={
            "cascade": "all, delete",
        },
    )


class Submission(SQLModel, table=True):
    __tablename__ = "submissions"

    id: int | None = Field(default=None, primary_key=True)

    submission_data: str
    evaluation: int | None = None
    team_id: int = Field(foreign_key="teams.id")
    task_id: int = Field(foreign_key="tasks.id")

    team: Team = Relationship(back_populates="submissions")
    task: Task = Relationship(back_populates="submissions")


class Hackathon(SQLModel, table=True):
    __tablename__ = "hackathons"

    id: int | None = Field(default=None, primary_key=True)

    name: str
    start_date: datetime.datetime
    end_date: datetime.datetime

    tasks: list[Task] = Relationship(
        back_populates="hackathon",
        sa_relationship_kwargs={
            "cascade": "all, delete",
        },
    )
    teams: list[Team] = Relationship(
        back_populates="hackathon",
        sa_relationship_kwargs={
            "cascade": "all, delete",
        },
    )