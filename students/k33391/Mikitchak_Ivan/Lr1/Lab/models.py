from sqlalchemy import Column, DateTime, UniqueConstraint
from sqlmodel import Relationship, SQLModel, Field

from typing import List, Optional
from pydantic import BaseModel, EmailStr, field_validator, model_validator

from datetime import datetime
import re
from enum import Enum


DATETIME_REGEX = r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}[+\-]\d{2}(:\d{2})?$"


class LoginForm(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: EmailStr = Field(unique=True, nullable=False, index=True)
    hashed_password: str
    last_logout: Optional[datetime] = Field(default=None, sa_column=Column(DateTime(timezone=True)))
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    
    organizers: List["Organizer"] = Relationship(back_populates="user", cascade_delete=True)
    participants: List["Participant"] = Relationship(back_populates="user", cascade_delete=True)
    
    def __str__(self):
        return (f"User ("
                f"\"id\": {id}, "
                f"\"email\": {self.email}, "
                f"\"first_name\": {self.first_name}, "
                f"\"last_name\": {self.last_name})")


class UserCreateForm(BaseModel):
    email: EmailStr
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None

    @field_validator("password")
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        if not any(char.isdigit() for char in value):
            raise ValueError("Password must contain at least one digit.")
        if not any(char.isupper() for char in value):
            raise ValueError(
                "Password must contain at least one uppercase letter.")
        if not any(char.islower() for char in value):
            raise ValueError(
                "Password must contain at least one lowercase letter.")
        return value


class UserUpdateEmailForm(BaseModel):
    email: EmailStr
    password: str


class UserUpdatePasswordForm(BaseModel):
    password: str
    new_password: str
    
    @field_validator("new_password")
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        if not any(char.isdigit() for char in value):
            raise ValueError("Password must contain at least one digit.")
        if not any(char.isupper() for char in value):
            raise ValueError(
                "Password must contain at least one uppercase letter.")
        if not any(char.islower() for char in value):
            raise ValueError(
                "Password must contain at least one lowercase letter.")
        return value


class UserUpdateForm(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserDeleteForm(BaseModel):
    password: str


class UserSerialized(BaseModel):
    id: int
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class Contest(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(nullable=False)
    code: str = Field(nullable=False)
    description: str = Field(nullable=False)
    start_date: datetime = Field(sa_column=Column(DateTime(timezone=True),  nullable=False))
    end_date: datetime = Field(sa_column=Column(DateTime(timezone=True), nullable=False))
    
    organizers: List["Organizer"] = Relationship(back_populates="contest", cascade_delete=True)
    participants: List["Participant"] = Relationship(back_populates="contest", cascade_delete=True)
    teams: List["Team"] = Relationship(back_populates="contest", cascade_delete=True)
    problems: List["Problem"] = Relationship(back_populates="contest", cascade_delete=True)
    
    @model_validator(mode="after")
    def validate_dates(self):
        if self.end_date <= self.start_date:
            raise ValueError("The end_date must be after the start_date.")
        
        return self
    
    def __str__(self):
        return (f"Contest ("
                f"\"id\": {self.id}, "
                f"\"title\": {self.title}, "
                f"\"description\": {self.description}, "
                f"\"start_date\": {self.start_date}, "
                f"\"end_date\": {self.end_date})")


class ContestCreateForm(BaseModel):
    title: str
    description: str
    start_date: str
    end_date: str

    @field_validator("start_date", "end_date")
    def validate_datetime_fields(cls, value):
        if value is None:
            return value
        
        # Validate with regex
        if not re.match(DATETIME_REGEX, value):
            raise ValueError(f"{value} must be in the format YYYY-MM-DD HH:MM:SS±HH or YYYY-MM-DD HH:MM:SS±HH:MM")
        
        # Normalize datetime string to include minutes in timezone offset if necessary
        if len(value) == 22 and value[-3] == '+':
            value += ':00'  # e.g., '2024-10-01 12:00:00+00' -> '2024-10-01 12:00:00+00:00'

        # Try parsing the datetime to ensure it's valid
        try:
            datetime.strptime(value, "%Y-%m-%d %H:%M:%S%z")
        except ValueError:
            raise ValueError(f"{value} is not a valid datetime")
        
        return value
    
    @model_validator(mode="after")
    def validate_dates(self):
        if self.start_date is not None:
            start_date = datetime.strptime(self.start_date, "%Y-%m-%d %H:%M:%S%z")
        else:
            start_date = None
        
        if self.end_date is not None:
            end_date = datetime.strptime(self.end_date, "%Y-%m-%d %H:%M:%S%z")
        else:
            end_date = None

        if start_date and end_date and end_date <= start_date:
            raise ValueError("The end_date must be after the start_date.")
        
        return self


class ContestUpdateForm(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    
    @field_validator("start_date", "end_date")
    def validate_datetime_fields(cls, value):
        if value is None:
            return value
        
        # Validate with regex
        if not re.match(DATETIME_REGEX, value):
            raise ValueError(f"{value} must be in the format YYYY-MM-DD HH:MM:SS±HH or YYYY-MM-DD HH:MM:SS±HH:MM")
        
        # Normalize datetime string to include minutes in timezone offset if necessary
        if len(value) == 22 and value[-3] == '+':
            value += ':00'  # e.g., '2024-10-01 12:00:00+00' -> '2024-10-01 12:00:00+00:00'

        # Try parsing the datetime to ensure it's valid
        try:
            datetime.strptime(value, "%Y-%m-%d %H:%M:%S%z")
        except ValueError:
            raise ValueError(f"{value} is not a valid datetime")
        
        return value
    
    @model_validator(mode="after")
    def validate_dates(self):
        if self.start_date is not None:
            start_date = datetime.strptime(self.start_date, "%Y-%m-%d %H:%M:%S%z")
        else:
            start_date = None
        
        if self.end_date is not None:
            end_date = datetime.strptime(self.end_date, "%Y-%m-%d %H:%M:%S%z")
        else:
            end_date = None

        if start_date and end_date and end_date <= start_date:
            raise ValueError("The end_date must be after the start_date.")
        
        return self


class ContestSerializedAdmin(BaseModel):
    id: int
    title: str
    code: str
    description: str
    start_date: datetime
    end_date: datetime


class ContestSerialized(BaseModel):
    id: int
    title: str
    description: str
    start_date: datetime
    end_date: datetime
    
    class Config:
        arbitrary_types_allowed = True


class ContestSerializedShort(BaseModel):
    id: int
    title: str


class OrganizerRole(Enum):
    admin = "admin"
    moderator = "moderator"


class Organizer(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
    user_id: int = Field(foreign_key="user.id", nullable=False, index=True)
    user: User = Relationship(back_populates="organizers")
    
    contest_id: int = Field(foreign_key="contest.id", nullable=False, index=True)
    contest: Contest = Relationship(back_populates="organizers")
    
    role: OrganizerRole
    
    __table_args__ = (
        UniqueConstraint("user_id", "contest_id", name="uq_user_contest_organizer"),
    )

    def __str__(self):
        return (f"Organizer ("
                f"\"id\": {self.id}, "
                f"\"user_id\": {self.user_id}, "
                f"\"contest_id\": {self.contest_id}, "
                f"\"role\": {self.role})")


class JoinAsOrganizerForm(BaseModel):
    code: str


class OrganizerSerialized(BaseModel):
    id: int
    user: UserSerialized
    role: OrganizerRole


class Participant(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
    user_id: int = Field(foreign_key="user.id", index=True, nullable=False)
    user: User = Relationship(back_populates="participants")
    
    contest_id: int = Field(foreign_key="contest.id", index=True, nullable=False)
    contest: Contest = Relationship(back_populates="participants")
    
    score: int = Field(default=0, nullable=False)
    
    team_member: Optional["TeamMember"] = Relationship(back_populates="participant", cascade_delete=True)
    submissions: List["Submission"] = Relationship(back_populates="participant", cascade_delete=True)
    
    __table_args__ = (
        UniqueConstraint("user_id", "contest_id", name="uq_user_contest_participant"),
    )
    
    @field_validator("score")
    def validate_score(cls, value):
        if value < 0 or value > 100:
            raise ValueError("Score must be in range [0, 100].")
        return value

    def __str__(self):
        return (f"Participant ("
                f"\"id\": {self.id}, "
                f"\"user_id\": {self.user_id}, "
                f"\"contest_id\": {self.contest_id}, "
                f"\"score\": {self.score})")


class ScoreParticipantForm(BaseModel):
    score: int
    
    @field_validator("score")
    def validate_score(cls, value):
        if value < 0 or value > 100:
            raise ValueError("Score must be in range [0, 100].")
        return value


class ParticipantSerialized(BaseModel):
    id: int
    user: UserSerialized
    score: int


class Team(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
    contest_id: int = Field(foreign_key="contest.id", nullable=False)
    contest: Contest = Relationship(back_populates="teams")
    
    name: str = Field(nullable=False)
    code: str = Field(nullable=False)
    
    team_members: List["TeamMember"] = Relationship(back_populates="team", cascade_delete=True)


class TeamForm(BaseModel):
    name: Optional[str] = None


class TeamSerialized(BaseModel):
    id: int
    name: str


class TeamSerializedOwner(BaseModel):
    id: int
    name: str
    code: str


class TeamRole(Enum):
    owner = "owner"
    member = "member"


class TeamMember(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
    participant_id: int = Field(foreign_key="participant.id", nullable=False)
    participant: Participant = Relationship(back_populates="team_member")
    
    team_id: int = Field(foreign_key="team.id", nullable=False)
    team: Team = Relationship(back_populates="team_members")
    
    role: TeamRole = Field(nullable=False)
    
    __table_args__ = (
        UniqueConstraint("participant_id", "team_id", name="uq_participant_team"),
    )
    
    @model_validator(mode="after")
    def validate_contest_participation(self):
        if self.team.contest_id != self.participant.contest_id:
            raise ValueError("team and participant must relate to the same contest")
        
        return self


class JoinTeamForm(BaseModel):
    code: str


class TeamMemberSerialized(BaseModel):
    id: int
    user: UserSerialized
    role: TeamRole


class Problem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
    contest_id: int = Field(nullable=False, foreign_key="contest.id")
    contest: Contest = Relationship(back_populates="problems")
    
    title: str
    description: str
    
    submissions: List["Submission"] = Relationship(back_populates="problem", cascade_delete=True)


class CreateProblemForm(BaseModel):
    title: str
    description: str


class UpdateProblemForm(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


class ProblemSerialized(BaseModel):
    id: int
    title: str
    description: str


class ProblemSerializedShort(BaseModel):
    id: int
    title: str


class Submission(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
    problem_id: int = Field(nullable=False, foreign_key="problem.id")
    problem: Problem = Relationship(back_populates="submissions")
    
    participant_id: int = Field(nullable=False, foreign_key="participant.id")
    participant: Participant = Relationship(back_populates="submissions")
    
    data: str = Field(nullable=False)
    date_submitted: datetime = Field(sa_column=Column(DateTime(timezone=True), default=datetime.now().astimezone(), nullable=False))


class SubmissionForm(BaseModel):
    data: str


class SubmissionSerialized(BaseModel):
    id: int
    participant: ParticipantSerialized
    data: str
    date_submitted: datetime


class SubmissionSerializedShort(BaseModel):
    id: int
    participant: ParticipantSerialized
    date_submitted: datetime


class SubmissionSerializedMy(BaseModel):
    id: int
    data: str
    date_submitted: datetime


class SubmissionSerializedMyShort(BaseModel):
    id: int
    date_submitted: datetime


class SubmissionSerializedTeam(BaseModel):
    id: int
    member: TeamMemberSerialized
    data: str
    date_submitted: datetime


class SubmissionSerializedTeamShort(BaseModel):
    id: int
    member: TeamMemberSerialized
    date_submitted: datetime
