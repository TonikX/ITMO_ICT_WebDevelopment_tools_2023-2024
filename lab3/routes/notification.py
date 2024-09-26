from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlmodel import select
from connection import get_session
from models import Notification

router = APIRouter()

@router.get("/notifications", response_model=List[Notification], tags=["notification"])
def get_notifications(session=Depends(get_session)) -> List[Notification]:
    return session.exec(select(Notification)).all()

@router.get("/notifications/{notification_id}", response_model=Notification, tags=["notification"])
def get_notification(notification_id: int, session=Depends(get_session)) -> Notification:
    notification = session.get(Notification, notification_id)
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    return notification

@router.post("/notifications", response_model=Notification, tags=["notification"])
def create_notification(notification: Notification, session=Depends(get_session)) -> Notification:
    session.add(notification)
    session.commit()
    session.refresh(notification)
    return notification

@router.patch("/notifications/{notification_id}", response_model=Notification, tags=["notification"])
def update_notification(notification_id: int, notification: Notification, session=Depends(get_session)) -> Notification:
    db_notification = session.get(Notification, notification_id)
    if not db_notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    notification_data = notification.dict(exclude_unset=True)
    for key, value in notification_data.items():
        setattr(db_notification, key, value)
    session.add(db_notification)
    session.commit()
    session.refresh(db_notification)
    return db_notification

@router.delete("/notifications/{notification_id}", tags=["notification"])
def delete_notification(notification_id: int, session=Depends(get_session)):
    notification = session.get(Notification, notification_id)
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    session.delete(notification)
    session.commit()
    return {"ok": True}
