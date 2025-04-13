from sqlmodel import Field, Relationship
from datetime import datetime

from src.api.notifications.default import NotificationDefault
from src.api.priorities.default import PriorityDefault
from src.api.schedule_tasks.default import ScheduleTaskDefault
from src.api.schedules.default import ScheduleDefault
from src.api.tasks.default import TaskDefault
from src.api.time_entries.default import TimeEntryDefault
from src.api.users.default import UserDefault


# Associative table
class ScheduleTask(ScheduleTaskDefault, table=True):
    added_at: datetime = Field(default_factory=datetime.utcnow)

# User table
class User(UserDefault, table=True):
    id: int | None = Field(default=None, primary_key=True)
    password_hash: str | None = None
    tasks: list["Task"] = Relationship(back_populates="user",
                                       sa_relationship_kwargs={"cascade": "delete"})
    schedules: list["Schedule"] = Relationship(back_populates="user",
                                               sa_relationship_kwargs={"cascade": "delete"})

# Priority table
class Priority(PriorityDefault, table=True):
    id: int | None = Field(default=None, primary_key=True)
    tasks: list["Task"] = Relationship(back_populates="priority",
                                       sa_relationship_kwargs={"cascade": "delete"})

# Task table
class Task(TaskDefault, table=True):
    id: int | None = Field(default=None, primary_key=True)
    priority: Priority | None = Relationship(back_populates="tasks")
    user: User | None = Relationship(back_populates="tasks")
    time_entries: list["TimeEntry"] = Relationship(back_populates="task",
                                                   sa_relationship_kwargs={"cascade": "delete"})
    notifications: list["Notification"] = Relationship(back_populates="task",
                                                       sa_relationship_kwargs={"cascade": "delete"})
    schedules: list["Schedule"] = Relationship(back_populates="tasks",
                                               link_model=ScheduleTask,
                                               sa_relationship_kwargs={"cascade": "delete"})

# TimeEntry table
class TimeEntry(TimeEntryDefault, table=True):
    id: int | None = Field(default=None, primary_key=True)
    task: Task | None = Relationship(back_populates="time_entries")

# Schedule table
class Schedule(ScheduleDefault, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user: User | None = Relationship(back_populates="schedules")
    tasks: list[Task] = Relationship(back_populates="schedules",
                                     link_model=ScheduleTask,
                                     sa_relationship_kwargs={"cascade": "delete"})

# Notification table
class Notification(NotificationDefault, table=True):
    id: int | None = Field(default=None, primary_key=True)
    task: Task | None = Relationship(back_populates="notifications")
