from src.api.tasks.default import TaskDefault
from src.db.models import Priority, Schedule, TimeEntry, User, Notification


# Task table
class TaskInner(TaskDefault):
    priority: Priority | None = None
    user: User | None = None
    time_entries: list[TimeEntry] | None = None
    notifications: list[Notification] | None = None
    schedules: list[Schedule] | None = None
