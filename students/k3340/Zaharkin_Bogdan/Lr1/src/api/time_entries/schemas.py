from src.api.time_entries.default import TimeEntryDefault
from src.db.models import Task


# TimeEntry table
class TimeEntryInner(TimeEntryDefault):
    task: Task | None = None
