from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlmodel import select
from connection import get_session
from models import TaskInfo

router = APIRouter()


@router.get("/taskinfo/list", response_model=List[TaskInfo], tags=["taskinfo"])
def taskinfo_list(session=Depends(get_session)) -> List[TaskInfo]:
    return session.exec(select(TaskInfo)).all()


@router.get("/taskinfo/{task_id}/{user_id}", response_model=TaskInfo, tags=["taskinfo"])
def get_task_info(task_id: int, user_id: int, session=Depends(get_session)) -> TaskInfo:
    task_info = session.query(TaskInfo).filter_by(task_id=task_id, user_id=user_id).first()
    if not task_info:
        raise HTTPException(status_code=404, detail="TaskInfo not found")
    return task_info


@router.patch("/taskinfo/{task_id}/{user_id}", response_model=TaskInfo, tags=["taskinfo"])
def taskinfo_update(task_id: int, user_id: int, task_info: TaskInfo, session=Depends(get_session)) -> TaskInfo:
    db_task_info = session.execute(
        select(TaskInfo).where(TaskInfo.task_id == task_id, TaskInfo.user_id == user_id)
    ).first()
    if not db_task_info:
        raise HTTPException(status_code=404, detail="TaskInfo not found")
    task_info_data = task_info.dict(exclude_unset=True)
    for key, value in task_info_data.items():
        setattr(db_task_info, key, value)
    session.add(db_task_info)
    session.commit()
    session.refresh(db_task_info)
    return db_task_info


@router.delete("/taskinfo/{task_id}/{user_id}", tags=["taskinfo"])
def taskinfo_delete(task_id: int, user_id: int, session=Depends(get_session)):
    task_info = session.execute(
        select(TaskInfo).where(TaskInfo.task_id == task_id, TaskInfo.user_id == user_id)
    ).first()
    if not task_info:
        raise HTTPException(status_code=404, detail="TaskInfo not found")
    session.delete(task_info)
    session.commit()
    return {"ok": True}


@router.post("/taskinfo/", response_model=TaskInfo, tags=["taskinfo"])
def create_task_info(task_info: TaskInfo, session=Depends(get_session)) -> TaskInfo:
    session.add(task_info)
    session.commit()
    session.refresh(task_info)
    return task_info
