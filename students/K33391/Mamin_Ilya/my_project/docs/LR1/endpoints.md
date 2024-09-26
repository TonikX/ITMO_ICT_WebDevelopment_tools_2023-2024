# Модуль эндпоинтов API

Этот модуль предоставляет эндпоинты для выполнения операций с задачами, расписаниями и напоминаниями.

## Описание

Модуль включает в себя эндпоинты API для создания, чтения, обновления и удаления задач, расписаний и напоминаний.

## Код

```python
import datetime
from fastapi import APIRouter, HTTPException, Depends
from models import (
    TaskDefault, Task, TaskShow,
    ScheduleDefault, ScheduleShow, Schedule,
    ReminderDefault, ReminderShow, Reminder,
    User
)
from db import get_session
from typing_extensions import TypedDict

logic_router = APIRouter()

@logic_router.post("/task-create")
def task_create(task: TaskDefault, session=Depends(get_session)) -> TypedDict('Response', {"status": int, "data": Task}):
    task = Task.model_validate(task)
    session.add(task)
    session.commit()
    session.refresh(task)
    return {"status": 200, "data": task}

@logic_router.get("/list-tasks")
def tasks_list(session=Depends(get_session)) -> list[Task]:
    return session.query(Task).all()

@logic_router.get("/task/{task_id}", response_model=TaskShow)
def task_get(task_id: int, session=Depends(get_session)):
    obj = session.get(Task, task_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="task not found")
    return obj

@logic_router.patch("/task/update/{task_id}")
def task_update(task_id: int, task: TaskDefault, session=Depends(get_session)) -> Task:
    db_task = session.get(Task, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="task not found")

    task_data = task.model_dump(exclude_unset=True)
    for key, value in task_data.items():
        setattr(db_task, key, value)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

@logic_router.delete("/task/delete/{task_id}")
def task_delete(task_id: int, session=Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="task not found")
    session.delete(task)
    session.commit()
    return {"ok": True}

@logic_router.post("/schedule-create")
def schedule_create(schedule: ScheduleDefault, session=Depends(get_session)) -> TypedDict('Response', {"status": int, "data": Schedule}):
    schedule = Schedule.model_validate(schedule)
    session.add(schedule)
    session.commit()
    session.refresh(schedule)
    return {"status": 200, "data": schedule}

@logic_router.get("/list-schedules")
def schedules_list(session=Depends(get_session)) -> list[Schedule]:
    return session.query(Schedule).all()

@logic_router.get("/schedule/{schedule_id}", response_model=ScheduleShow)
def schedule_get(schedule_id: int, session=Depends(get_session)):
    obj = session.get(Schedule, schedule_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="schedule not found")
    return obj

@logic_router.patch("/schedule/update/{schedule_id}")
def schedule_update(schedule_id: int, schedule: ScheduleDefault, session=Depends(get_session)) -> Schedule:
    db_schedule = session.get(Schedule, schedule_id)
    if not db_schedule:
        raise HTTPException(status_code=404, detail="schedule not found")

    schedule_data = schedule.model_dump(exclude_unset=True)
    for key, value in schedule_data.items():
        setattr(db_schedule, key, value)
    session.add(db_schedule)
    session.commit()
    session.refresh(db_schedule)
    return db_schedule

@logic_router.delete("/schedule/delete/{schedule_id}")
def schedule_delete(schedule_id: int, session=Depends(get_session)):
    schedule = session.get(Schedule, schedule_id)
    if not schedule:
        raise HTTPException(status_code=404, detail="schedule not found")
    session.delete(schedule)
    session.commit()
    return {"ok": True}

@logic_router.post("/reminder-create")
def reminder_create(reminder: ReminderDefault, session=Depends(get_session)) -> TypedDict('Response', {"status": int, "data": Reminder}):
    reminder = Reminder.model_validate(reminder)
    session.add(reminder)
    session.commit()
    session.refresh(reminder)
    return {"status": 200, "data": reminder}

@logic_router.get("/list-reminders")
def reminders_list(session=Depends(get_session)) -> list[Reminder]:
    return session.query(Reminder).all()

@logic_router.get("/reminder/{reminder_id}", response_model=ReminderShow)
def reminder_get(reminder_id: int, session=Depends(get_session)):
    obj = session.get(Reminder, reminder_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="reminder not found")
    return obj

@logic_router.patch("/reminder/update/{reminder_id}")
def reminder_update(reminder_id: int, reminder: ReminderDefault, session=Depends(get_session)) -> Reminder:
    db_reminder = session.get(Reminder, reminder_id)
    if not db_reminder:
        raise HTTPException(status_code=404, detail="reminder not found")

    reminder_data = reminder.model_dump(exclude_unset=True)
    for key, value in reminder_data.items():
        setattr(db_reminder, key, value)
    session.add(db_reminder)
    session.commit()
    session.refresh(db_reminder)
    return db_reminder

@logic_router.delete("/reminder/delete/{reminder_id}")
def reminder_delete(reminder_id: int, session=Depends(get_session)):
    reminder = session.get(Reminder, reminder_id)
    if not reminder:
        raise HTTPException(status_code=404, detail="reminder not found")
    session.delete(reminder)
    session.commit()
    return {"ok": True}

@logic_router.get("/user/{user_id}/schedules")
def user_schedules(user_id: int, session=Depends(get_session)) -> list[Schedule]:
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    return session.query(Schedule).filter(Schedule.user_id == user_id).all()

@logic_router.patch("/task/{task_id}/add-time")
def add_time_to_task(task_id: int, time_spent: int, session=Depends(get_session)) -> Task:
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="task not found")
    if task.time_spent is None:
        task.time_spent = 0
    task.time_spent += time_spent
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

@logic_router.get("/user/{user_id}/time-analysis")
def user_time_analysis(user_id: int, session=Depends(get_session)) -> TypedDict('Response', {"status": int, "time_spent": dict}):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    tasks = session.query(Task).filter(Task.user_id == user_id).all()
    time = { task.id: task.time_spent if task.time_spent is not None else 0 for task in tasks }
    return {"status": 200, "time_spent": time}

@logic_router.post("/reminder/{reminder_id}/copy-for-task/{task_id}")
def copy_reminder_for_task(reminder_id: int, task_id: int, session=Depends(get_session)):
    reminder = session.get(Reminder, reminder_id)
    if not reminder:
        raise HTTPException(status_code=404, detail="reminder not found")
    
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="task not found")
    
    new_reminder = Reminder(
        task_id=task_id,
        remind_at=reminder.remind_at,
        user_id=reminder.user_id
    )
    session.add(new_reminder)
    session.commit()
    session.refresh(new_reminder)
    return {"status": 200, "message": "Reminder copied for new task successfully"}
```