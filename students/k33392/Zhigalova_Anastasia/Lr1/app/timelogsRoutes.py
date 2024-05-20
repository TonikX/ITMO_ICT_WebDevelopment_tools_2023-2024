from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import Session, select, SQLModel
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.future import select
from conn import get_session, init_db
from models import * 
from typing import List

from pydanticModels import *

router = APIRouter()

@router.post("/timelogs/", response_model=TimeLog)
def create_timelog(timelog: TimeLogCreate, session: Session = Depends(get_session)):  
    task = session.get(Task, timelog.task_id)
    if not task:
        raise HTTPException(status_code=404, detail=f"Task with id {timelog.task_id} not found")

    db_timelog = TimeLog(**timelog.dict())  
    session.add(db_timelog)
    try:
        session.commit()
    except Exception as e:
        session.rollback()  
        raise HTTPException(status_code=400, detail=str(e))
    session.refresh(db_timelog)
    return db_timelog


@router.get("/timelogs/{timelog_id}", response_model=TimeLog)
def read_timelog(timelog_id: int, session: Session = Depends(get_session)):
    timelog = session.query(TimeLog).filter(TimeLog.id == timelog_id).first()
    if not timelog:
        raise HTTPException(status_code=404, detail="TimeLog not found")
    return timelog


@router.get("/timelogs/", response_model=List[TimeLog])
def read_timelogs(session: Session = Depends(get_session)):
    return session.query(TimeLog).all()

@router.put("/timelogs/{timelog_id}", response_model=TimeLog)
def update_timelog(timelog_id: int, timelog: TimeLogCreate, session: Session = Depends(get_session)):
    db_timelog = session.query(TimeLog).filter(TimeLog.id == timelog_id).first()
    if not db_timelog:
        raise HTTPException(status_code=404, detail="TimeLog not found")
    for var, value in vars(timelog).items():
        setattr(db_timelog, var, value) if value else None
    session.commit()
    session.refresh(db_timelog)  
    return db_timelog

@router.delete("/timelogs/{timelog_id}", response_model=dict)
def delete_timelog(timelog_id: int, session: Session = Depends(get_session)):
    timelog = session.get(TimeLog, timelog_id)
    if not timelog:
        raise HTTPException(status_code=404, detail="TimeLog not found")
    session.delete(timelog)
    session.commit()
    return {"ok": True}
