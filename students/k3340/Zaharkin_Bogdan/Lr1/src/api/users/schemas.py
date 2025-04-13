from src.api.users.default import UserDefault
from src.db.models import Schedule, Task


# User table
class UserInner(UserDefault):
    tasks: list[Task] | None = None
    schedules: list[Schedule] | None = None
