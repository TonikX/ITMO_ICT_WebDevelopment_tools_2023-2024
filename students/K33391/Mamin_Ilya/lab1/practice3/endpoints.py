import datetime
from fastapi import APIRouter, HTTPException, Depends
from models import (
    TaskDefault, Task, TaskShow,
    ScheduleDefault, ScheduleShow, Schedule,
    ReminderDefault, ReminderShow, Reminder,
)
from db import get_session
from pydantic import BaseModel
from sqlalchemy.orm import joinedload

class Response(BaseModel):
    status: int
    data: dict

logic_router = APIRouter()

@logic_router.post("/task-create", response_model=Response)
def task_create(task: TaskDefault, session=Depends(get_session)) -> Response:
    db_task = Task(**task.dict())
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return {"status": 200, "data": db_task.dict()}

@logic_router.get("/list-tasks", response_model=list[TaskShow])
def tasks_list(session=Depends(get_session)) -> list[TaskShow]:
    return session.query(Task).all()

@logic_router.get("/task/{task_id}", response_model=TaskShow)
def task_get(task_id: int, session=Depends(get_session)):
    obj = session.get(Task, task_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return obj.dict()

@logic_router.patch("/task/update/{task_id}", response_model=TaskShow)
def task_update(task_id: int, task: TaskDefault, session=Depends(get_session)):
    db_task = session.get(Task, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    task_data = task.dict(exclude_unset=True)
    for key, value in task_data.items():
        setattr(db_task, key, value)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

@logic_router.delete("/task/delete/{task_id}", response_model=dict)
def task_delete(task_id: int, session=Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    session.delete(task)
    session.commit()
    return {"ok": True}

@logic_router.post("/schedule-create", response_model=Response)
def schedule_create(schedule: ScheduleDefault, session=Depends(get_session)) -> Response:
    db_schedule = Schedule(**schedule.dict())
    session.add(db_schedule)
    session.commit()
    session.refresh(db_schedule)
    return {"status": 200, "data": db_schedule.dict()}

@logic_router.get("/list-schedules", response_model=list[ScheduleShow])
def schedules_list(session=Depends(get_session)) -> list[ScheduleShow]:
    return session.query(Schedule).all()

@logic_router.get("/schedule/{schedule_id}", response_model=ScheduleShow)
def schedule_get(schedule_id: int, session=Depends(get_session)):
    obj = session.get(Schedule, schedule_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return obj

@logic_router.patch("/schedule/update/{schedule_id}", response_model=ScheduleShow)
def schedule_update(schedule_id: int, schedule: ScheduleDefault, session=Depends(get_session)):
    db_schedule = session.get(Schedule, schedule_id)
    if not db_schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")

    schedule_data = schedule.dict(exclude_unset=True)
    for key, value in schedule_data.items():
        setattr(db_schedule, key, value)
    session.add(db_schedule)
    session.commit()
    session.refresh(db_schedule)
    return db_schedule

@logic_router.delete("/schedule/delete/{schedule_id}", response_model=dict)
def schedule_delete(schedule_id: int, session=Depends(get_session)):
    schedule = session.get(Schedule, schedule_id)
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    session.delete(schedule)
    session.commit()
    return {"ok": True}

@logic_router.post("/reminder-create", response_model=Response)
def reminder_create(reminder: ReminderDefault, session=Depends(get_session)) -> Response:
    db_reminder = Reminder(**reminder.dict())
    session.add(db_reminder)
    session.commit()
    session.refresh(db_reminder)
    return {"status": 200, "data": db_reminder.dict()}

@logic_router.get("/list-reminders", response_model=list[ReminderShow])
def reminders_list(session=Depends(get_session)) -> list[ReminderShow]:
    reminders = session.query(Reminder).options(joinedload(Reminder.task)).all()
    return reminders

@logic_router.get("/reminder/{reminder_id}", response_model=ReminderShow)
def reminder_get(reminder_id: int, session=Depends(get_session)) -> ReminderShow:
    obj = session.query(Reminder).options(joinedload(Reminder.task)).filter(Reminder.id == reminder_id).first()
    
    if obj is None:
        raise HTTPException(status_code=404, detail="Reminder not found")
    
    return obj

@logic_router.patch("/reminder/update/{reminder_id}", response_model=ReminderShow)
def reminder_update(reminder_id: int, reminder: ReminderDefault, session=Depends(get_session)):
    db_reminder = session.get(Reminder, reminder_id)
    if not db_reminder:
        raise HTTPException(status_code=404, detail="Reminder not found")

    reminder_data = reminder.dict(exclude_unset=True)
    for key, value in reminder_data.items():
        setattr(db_reminder, key, value)
    session.add(db_reminder)
    session.commit()
    session.refresh(db_reminder)
    return db_reminder.dict()

@logic_router.delete("/reminder/delete/{reminder_id}", response_model=dict)
def reminder_delete(reminder_id: int, session=Depends(get_session)):
    reminder = session.get(Reminder, reminder_id)
    if not reminder:
        raise HTTPException(status_code=404, detail="Reminder not found")
    session.delete(reminder)
    session.commit()
    return {"ok": True}

@logic_router.patch("/task/{task_id}/add-time", response_model=TaskShow)
def add_time_to_task(task_id: int, time_spent: int, session=Depends(get_session)) -> TaskShow:
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.time_spent is None:
        task.time_spent = 0
    task.time_spent += time_spent
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

@logic_router.post("/reminder/{reminder_id}/copy-for-task/{task_id}", response_model=dict)
def copy_reminder_for_task(reminder_id: int, task_id: int, session=Depends(get_session)) -> dict:
    reminder = session.get(Reminder, reminder_id)
    if not reminder:
        raise HTTPException(status_code=404, detail="Reminder not found")
    
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    new_reminder = Reminder(
        task_id=task_id,
        remind_at=reminder.remind_at
    )
    session.add(new_reminder)
    session.commit()
    session.refresh(new_reminder)
    return {"status": 200, "message": "Reminder copied for new task successfully"}