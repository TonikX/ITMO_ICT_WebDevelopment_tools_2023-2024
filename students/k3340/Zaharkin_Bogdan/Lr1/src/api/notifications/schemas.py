from src.api.notifications.default import NotificationDefault
from src.db.models import Task


# Notification table
class NotificationInner(NotificationDefault):
    task: Task | None = None
