from src.api.schedules.default import ScheduleDefault
from src.db.models import Task, User


# Schedule table
class ScheduleInner(ScheduleDefault):
    user: User | None = None
    tasks: list[Task] | None = None
