from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import selectinload
from sqlmodel import Session, select, create_engine
from starlette import status


import os
from dotenv import load_dotenv
from models import *

app = FastAPI()

load_dotenv()

DATABASE_URL = os.getenv("DB_ADMIN")
engine = create_engine(DATABASE_URL)


@app.on_event("startup")
def on_startup():
    init_db()


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


@app.post("/tasks/", response_model=TaskResponse)
def create_task(task: CreateTask, session: Session = Depends(get_session)):
    db_task = Task.from_orm(task)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


@app.get("/tasks/", response_model=List[TaskResponse])
def read_tasks(session: Session = Depends(get_session)):
    tasks = session.exec(select(Task).options(selectinload(Task.schedules))).all()
    return tasks


@app.post("/schedules/", response_model=ScheduleResponse)
def create_schedule(schedule: CreateSchedule, session: Session = Depends(get_session)):
    db_schedule = Schedule.from_orm(schedule)
    session.add(db_schedule)
    session.commit()
    session.refresh(db_schedule)
    return db_schedule


@app.get("/schedules/", response_model=List[ScheduleResponse])
def read_schedules(session: Session = Depends(get_session)):
    schedules = session.exec(
        select(Schedule).options(selectinload(Schedule.tasks))
    ).all()
    return schedules


@app.patch("/tasks/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int, task_update: UpdateTask, session: Session = Depends(get_session)
):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task_data = task_update.dict(exclude_unset=True)
    for key, value in task_data.items():
        setattr(task, key, value)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    session.delete(task)
    session.commit()
    return {"ok": True}


@app.post("/tasks/{task_id}/schedules/{schedule_id}")
def link_task_schedule(
    task_id: int, schedule_id: int, session: Session = Depends(get_session)
):
    link = TaskScheduleLink(task_id=task_id, schedule_id=schedule_id)
    session.add(link)
    session.commit()
    return {"message": "Task and Schedule linked successfully"}
