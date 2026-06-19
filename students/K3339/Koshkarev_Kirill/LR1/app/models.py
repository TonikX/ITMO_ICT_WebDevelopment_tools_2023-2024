"""Модели данных (таблицы) системы проведения хакатонов.

Структура БД (7 таблиц):
  users        — участники / организаторы / судьи
  hackathons   — сами хакатоны
  teams        — команды (привязаны к хакатону)        [one-to-many: hackathon -> teams]
  team_members — ассоциативная сущность User<->Team    [many-to-many + поле role_in_team]
  tasks        — задачи хакатона                       [one-to-many: hackathon -> tasks]
  submissions  — загруженные работы команд             [one-to-many: team -> submissions, task -> submissions]
  evaluations  — ассоциативная сущность Submission<->User(judge)  [many-to-many + поля score, comment]
"""
import enum
from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from app.database import Base


class UserRole(str, enum.Enum):
    """Роль пользователя в системе."""
    participant = "participant"  # участник
    organizer = "organizer"      # организатор (публикует задачи, подтверждает регистрацию)
    judge = "judge"              # судья (оценивает работы)


class HackathonStatus(str, enum.Enum):
    planned = "planned"
    active = "active"
    finished = "finished"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(120), nullable=False)
    email = Column(String(120), unique=True, index=True, nullable=False)
    phone = Column(String(30), nullable=True)
    hashed_password = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.participant, nullable=False)
    # Подтверждение регистрации организаторами.
    is_confirmed = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Связи
    memberships = relationship("TeamMember", back_populates="user", cascade="all, delete-orphan")
    evaluations = relationship("Evaluation", back_populates="judge", cascade="all, delete-orphan")


class Hackathon(Base):
    __tablename__ = "hackathons"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    location = Column(String(200), nullable=True)
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    status = Column(Enum(HackathonStatus), default=HackathonStatus.planned, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # one-to-many
    tasks = relationship("Task", back_populates="hackathon", cascade="all, delete-orphan")
    teams = relationship("Team", back_populates="hackathon", cascade="all, delete-orphan")


class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False)
    description = Column(Text, nullable=True)
    hackathon_id = Column(Integer, ForeignKey("hackathons.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Имя команды уникально в рамках одного хакатона.
    __table_args__ = (UniqueConstraint("name", "hackathon_id", name="uq_team_name_per_hackathon"),)

    hackathon = relationship("Hackathon", back_populates="teams")
    members = relationship("TeamMember", back_populates="team", cascade="all, delete-orphan")
    submissions = relationship("Submission", back_populates="team", cascade="all, delete-orphan")


class TeamMember(Base):
    """Ассоциативная сущность связи многие-ко-многим User <-> Team.

    Помимо ссылок на таблицы содержит характеризующее связь поле role_in_team
    (роль участника в конкретной команде: программист, дизайнер, капитан и т.д.).
    """
    __tablename__ = "team_members"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    # Характеризующее связь поле.
    role_in_team = Column(String(80), nullable=False, default="member")
    joined_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Один пользователь не может состоять в одной команде дважды.
    __table_args__ = (UniqueConstraint("user_id", "team_id", name="uq_user_team"),)

    user = relationship("User", back_populates="memberships")
    team = relationship("Team", back_populates="members")


class Task(Base):
    """Задача (проект) хакатона. one-to-many: один хакатон -> много задач."""
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    hackathon_id = Column(Integer, ForeignKey("hackathons.id"), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    requirements = Column(Text, nullable=True)
    evaluation_criteria = Column(Text, nullable=True)
    max_score = Column(Float, default=100.0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    hackathon = relationship("Hackathon", back_populates="tasks")
    submissions = relationship("Submission", back_populates="task", cascade="all, delete-orphan")


class Submission(Base):
    """Загруженная командой работа (прототип) по конкретной задаче."""
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    repo_url = Column(String(300), nullable=True)
    submitted_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    team = relationship("Team", back_populates="submissions")
    task = relationship("Task", back_populates="submissions")
    evaluations = relationship("Evaluation", back_populates="submission", cascade="all, delete-orphan")


class Evaluation(Base):
    """Ассоциативная сущность связи многие-ко-многим Submission <-> User(судья).

    Характеризующие связь поля: score (оценка) и comment (комментарий судьи).
    """
    __tablename__ = "evaluations"

    id = Column(Integer, primary_key=True, index=True)
    submission_id = Column(Integer, ForeignKey("submissions.id"), nullable=False)
    judge_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    # Характеризующие связь поля.
    score = Column(Float, nullable=False)
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Один судья оценивает одну работу один раз.
    __table_args__ = (UniqueConstraint("submission_id", "judge_id", name="uq_submission_judge"),)

    submission = relationship("Submission", back_populates="evaluations")
    judge = relationship("User", back_populates="evaluations")
