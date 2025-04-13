from src.api.priorities.default import PriorityDefault
from src.db.models import Task


# Priority table
class PriorityInner(PriorityDefault):
    tasks: list[Task] | None = None
