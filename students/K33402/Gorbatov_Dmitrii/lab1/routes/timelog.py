from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlmodel import select
from connection import get_session
from models import TimeLog

router = APIRouter()

@router.get("/timelog/list", response_model=List[TimeLog], tags=["timelog"])
def timelog_list(session=Depends(get_session)) -> List[TimeLog]:
    return session.exec(select(TimeLog)).all()

@router.get("/timelog/{time_log_id}", response_model=TimeLog, tags=["timelog"])
def timelog_read(time_log_id: int, session=Depends(get_session)) -> TimeLog:
    timelog = session.get(TimeLog, time_log_id)
    if not timelog:
        raise HTTPException(status_code=404, detail="TimeLog not found")
    return timelog

@router.patch("/timrlog/{time_log_id}", response_model=TimeLog, tags=["timelog"])
def timelog_update(time_log_id: int, timelog: TimeLog, session=Depends(get_session)) -> TimeLog:
    db_timelog = session.get(TimeLog, time_log_id)
    if not db_timelog:
        raise HTTPException(status_code=404, detail="TimeLog not found")
    timelog_data = timelog.dict(exclude_unset=True)
    for key, value in timelog_data.items():
        setattr(db_timelog, key, value)
    session.add(db_timelog)
    session.commit()
    session.refresh(db_timelog)
    return db_timelog

@router.delete("/timelog/{time_log_id}", tags=["timelog"])
def timelog_delete(time_log_id: int, session=Depends(get_session)):
    timelog = session.get(TimeLog, time_log_id)
    if not timelog:
        raise HTTPException(status_code=404, detail="TimeLog not found")
    session.delete(timelog)
    session.commit()
    return {"ok": True}

@router.post("/timelog/", response_model=TimeLog, tags=["timelog"])
def create_time_log(time_log: TimeLog, session = Depends(get_session)) -> TimeLog:
    session.add(time_log)
    session.commit()
    session.refresh(time_log)
    return time_log
