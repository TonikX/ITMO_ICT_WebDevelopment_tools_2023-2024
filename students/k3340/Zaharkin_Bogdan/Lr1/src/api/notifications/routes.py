from fastapi import APIRouter, Depends

from src.api.generic import Response, create_object, delete_object, read_object, read_object_list, update_object
from src.api.notifications.default import NotificationDefault
from src.api.notifications.schemas import NotificationInner
from src.db.connection import get_session
from src.db.models import Notification


router = APIRouter(prefix="/notifications", tags=["notifications"])


# CRUD for Notification
@router.post("/")
def create_notification(notification: NotificationDefault, session=Depends(get_session)) -> Response[Notification]:
    """
    Create a new notification.

    - **notification**: NotificationDefault object containing notification details.
    - **session**: Database session dependency.

    Returns:
        Response[Notification]: The created notification.
    """
    return create_object(session, notification, Notification)

@router.get("/")
def get_notifications(session=Depends(get_session)) -> list[Notification]:
    """
    Get a list of all notifications.

    - **session**: Database session dependency.

    Returns:
        list[Notification]: List of notifications.
    """
    return read_object_list(session, Notification)

@router.get("/{notification_id}", response_model=NotificationInner)
def get_notification(notification_id: int, session=Depends(get_session)) -> Notification:
    """
    Get a notification by ID.

    - **notification_id**: ID of the notification to retrieve.
    - **session**: Database session dependency.

    Returns:
        Notification: The notification with the specified ID.
    """
    return read_object(session, notification_id, Notification)

@router.patch("/{notification_id}")
def update_notification(notification_id: int, notification: NotificationDefault, session=Depends(get_session)) -> NotificationDefault:
    """
    Update a notification by ID.

    - **notification_id**: ID of the notification to update.
    - **notification**: NotificationDefault object containing updated notification details.
    - **session**: Database session dependency.

    Returns:
        NotificationDefault: The updated notification.
    """
    return update_object(session, notification_id, notification, Notification)

@router.delete("/{notification_id}")
def delete_notification(notification_id: int, session=Depends(get_session)) -> dict:
    """
    Delete a notification by ID.

    - **notification_id**: ID of the notification to delete.
    - **session**: Database session dependency.

    Returns:
        dict: A dictionary indicating the result of the deletion.
    """
    return delete_object(session, notification_id, Notification)
