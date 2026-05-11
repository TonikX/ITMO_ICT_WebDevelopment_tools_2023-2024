from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.api.deps import get_current_user
from app.db.session import get_session
from app.models.notification import Notification
from app.models.task import Task
from app.models.user import User
from app.schemas.notification import NotificationCreate, NotificationRead, NotificationUpdate

router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.get("", response_model=list[NotificationRead])
def list_notifications(
    is_read: bool | None = None,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> list[NotificationRead]:
    query = select(Notification).where(Notification.user_id == current_user.id)
    if is_read is not None:
        query = query.where(Notification.is_read == is_read)
    items = session.exec(query).all()
    return [NotificationRead.model_validate(item) for item in items]


@router.get("/{notification_id}", response_model=NotificationRead)
def get_notification(
    notification_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> NotificationRead:
    item = session.exec(
        select(Notification).where(Notification.id == notification_id, Notification.user_id == current_user.id)
    ).first()
    if not item:
        raise HTTPException(status_code=404, detail="Notification not found")
    return NotificationRead.model_validate(item)


@router.post("", response_model=NotificationRead, status_code=status.HTTP_201_CREATED)
def create_notification(
    payload: NotificationCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> NotificationRead:
    if payload.task_id is not None:
        task = session.exec(select(Task).where(Task.id == payload.task_id, Task.user_id == current_user.id)).first()
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
    item = Notification.model_validate(payload, update={"user_id": current_user.id})
    session.add(item)
    session.commit()
    session.refresh(item)
    return NotificationRead.model_validate(item)


@router.patch("/{notification_id}", response_model=NotificationRead)
def update_notification(
    notification_id: int,
    payload: NotificationUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> NotificationRead:
    item = session.exec(
        select(Notification).where(Notification.id == notification_id, Notification.user_id == current_user.id)
    ).first()
    if not item:
        raise HTTPException(status_code=404, detail="Notification not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(item, key, value)
    session.add(item)
    session.commit()
    session.refresh(item)
    return NotificationRead.model_validate(item)


@router.delete("/{notification_id}")
def delete_notification(
    notification_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> dict[str, bool]:
    item = session.exec(
        select(Notification).where(Notification.id == notification_id, Notification.user_id == current_user.id)
    ).first()
    if not item:
        raise HTTPException(status_code=404, detail="Notification not found")
    session.delete(item)
    session.commit()
    return {"ok": True}
