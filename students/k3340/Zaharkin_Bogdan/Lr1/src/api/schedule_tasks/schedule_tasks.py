from fastapi import HTTPException
from sqlmodel import Session

from src.api.generic import Response
from src.db.models import Schedule, ScheduleTask, Task

def create_st(schedule_id: int, task_id: int, session: Session) -> Response[ScheduleTask]:
    schedule = session.get(Schedule, schedule_id)
    task = session.get(Task, task_id)
    if not schedule or not task:
        raise HTTPException(status_code=404, detail="Schedule or Task not found")
    schedule_task = ScheduleTask(schedule_id=schedule_id, task_id=task_id)
    session.add(schedule_task)
    session.commit()
    session.refresh(schedule_task)
    return {"status": 201, "data": schedule_task}

def get_st(schedule_id: int, task_id: int, session: Session) -> ScheduleTask:
    schedule_task = session.get(ScheduleTask, (schedule_id, task_id))
    if not schedule_task:
        raise HTTPException(status_code=404, detail="Pair Schedule and Task not found")
    return schedule_task

def delete_st(schedule_id: int, task_id: int, session: Session) -> dict:
    schedule_task = session.get(ScheduleTask, (schedule_id, task_id))
    if not schedule_task:
        raise HTTPException(status_code=404, detail="ScheduleTask not found")
    session.delete(schedule_task)
    session.commit()
    return {"ok": True}
