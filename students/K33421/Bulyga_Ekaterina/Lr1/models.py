from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship


class TaskUser(SQLModel, table=True):
    tasks: Optional[int] = Field(
        default=None, foreign_key="task.id", primary_key=True
    )
    user: Optional[str] = Field(
        default=None, foreign_key="user.username", primary_key=True
    )


class User(SQLModel, table=True):
    username: str = Field(default=None, primary_key=True)
    name: str
    surname: str
    patronymic: str
    hashed_password: str
    comments: List["Comment"] = Relationship(back_populates="user")
    tasks: List["Task"] = Relationship(back_populates="user", link_model=TaskUser)
    task_creator: List["Task"] = Relationship(back_populates="creator")


class TimetableWeek(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    date_start: datetime
    date_end: datetime
    days: List["TimetableDay"] = Relationship(back_populates="week")


class TimetableDayDefault(SQLModel):
    date: datetime
    week_id: Optional[int] = Field(default=None, foreign_key="timetableweek.id")


class TimetableDayWeek(TimetableDayDefault):
    week: Optional[TimetableWeek] = None


class TimetableDay(TimetableDayDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    week: Optional[TimetableWeek] = Relationship(back_populates="days")
    tasks: List["Task"] = Relationship(back_populates="day")


class TaskNotification(SQLModel, table=True):
    task_id: Optional[int] = Field(
        default=None, foreign_key="task.id", primary_key=True
    )
    notification_id: Optional[int] = Field(
        default=None, foreign_key="notification.id", primary_key=True
    )


class Notification(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    datetime: datetime
    tasks: List["Task"] = Relationship(back_populates="notification", link_model=TaskNotification)


class TaskDefault(SQLModel):
    title: str
    description: str
    day_id: Optional[int] = Field(default=None, foreign_key="timetableday.id")
    time_start: datetime
    planned_time_end: datetime
    time_end: datetime | None
    priority: int
    creator_id: str = Field(default=None, foreign_key="user.username")


class TaskDayNotificationsUser(TaskDefault):
    day: Optional[TimetableDay] = None
    notification: Optional[List[Notification]] = [None]
    user: Optional[List[User]] = [None]
    creator: Optional[User]


class Task(TaskDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    day: Optional[TimetableDay] = Relationship(back_populates="tasks")
    notification: Optional[List[Notification]] | None = Relationship(back_populates="tasks", link_model=TaskNotification)
    comments: List["Comment"] | None = Relationship(back_populates="task")
    user: Optional[List[User]] | None = Relationship(back_populates="tasks", link_model=TaskUser)
    creator: Optional[User] | None = Relationship(back_populates="task_creator")


class CommentDefault(SQLModel):
    text: str
    file: bytes | None
    created_at: datetime
    user_id: Optional[str] = Field(default=None, foreign_key="user.username")
    task_id: Optional[int] = Field(default=None, foreign_key="task.id")


class CommentUserTask(CommentDefault):
    user: Optional[User] = None
    task: Optional[Task] = None


class Comment(CommentDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    user: Optional[User] = Relationship(back_populates="comments")
    task: Optional[Task] = Relationship(back_populates="comments")
