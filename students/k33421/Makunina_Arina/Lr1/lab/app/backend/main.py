from datetime import datetime
from typing import List, Optional

from fastapi import HTTPException, Depends, Response
from sqlmodel import Session, select, delete
from starlette import status
from .app import app
from ..endpoints import auth
from sqlmodel import SQLModel
from .database import engine, get_session

app.include_router(auth.router)


from .models import (
    TaskResponse,
    CreateTask,
    ScheduleResponse,
    CreateSchedule,
    ScheduleBase,
    TimeAnalysis,
    CreateTimeAnalysis,
    TimeAnalysisResponse,
)
from .models import Task, Schedule, TaskScheduleLink, UpdateTask, User


@app.on_event("startup")
def on_startup():
    init_db()  # Регистрирует функцию `init_db` для выполнения при запуске приложения FastAPI


def init_db():
    SQLModel.metadata.create_all(engine)  # создает все таблицы в бд


@app.post("/tasks/", response_model=TaskResponse)
def create_task(
    task_data: CreateTask,
    session: Session = Depends(get_session),
    current_user: User = Depends(auth.get_current_user),
):
    db_task = Task.from_orm(task_data)  # Создает объект задачи из полученных данных
    db_task.user_id = current_user.id  # Присваивает задаче ID текущего пользователя
    session.add(db_task)  # Добавляет задачу в сессию бд
    session.commit()  # Фиксирует изменения в бд
    session.refresh(db_task)  # Обновляет объект
    return TaskResponse(  # Возвращает данные созданной задачи
        id=db_task.id,
        title=db_task.title,
        description=db_task.description,
        priority=db_task.priority,
        status=db_task.status,
        user_id=db_task.user_id,
    )


@app.get("/tasks/", response_model=List[TaskResponse])
def read_tasks(session: Session = Depends(get_session)):
    tasks = session.exec(select(Task)).all()
    return tasks


@app.post("/schedules/", response_model=ScheduleBase)
def create_schedule(
    schedule_data: CreateSchedule,
    session: Session = Depends(get_session),
    current_user: User = Depends(auth.get_current_user),
):
    db_schedule = Schedule(date=schedule_data.date, user_id=current_user.id)
    session.add(db_schedule)
    session.commit()
    session.refresh(db_schedule)
    for task_id in schedule_data.tasks:
        db_task = (
            session.query(Task)
            .filter(Task.id == task_id, Task.user_id == current_user.id)
            .first()
        )
        if not db_task:
            raise HTTPException(
                status_code=404,
                detail=f"Task with id {task_id} not found or not owned by the user",
            )
        db_task_schedule_link = TaskScheduleLink(
            task_id=task_id, schedule_id=db_schedule.id
        )
        session.add(db_task_schedule_link)
    session.commit()
    return ScheduleBase.from_orm(db_schedule)


@app.get("/schedules/", response_model=List[ScheduleResponse])
async def read_schedules(
    schedule_id: Optional[int] = None,
    session: Session = Depends(get_session),
    current_user: User = Depends(auth.get_current_user),
):
    if schedule_id:
        schedule = session.get(Schedule, schedule_id)
        if not schedule or schedule.user_id != current_user.id:
            raise HTTPException(
                status_code=404, detail="Schedule not found or not owned by the user"
            )
        session.refresh(schedule, attribute_names=["tasks"])
        tasks_responses = [TaskResponse.from_orm(task) for task in schedule.tasks]
        sched_response = ScheduleResponse(
            id=schedule.id,
            date=schedule.date,
            tasks=tasks_responses,
        )
        return [sched_response]
    schedules = session.exec(
        select(Schedule).where(Schedule.user_id == current_user.id)
    ).all()
    schedule_responses = []
    for sched in schedules:
        session.refresh(sched, attribute_names=["tasks"])

        tasks_responses = [TaskResponse.from_orm(task) for task in sched.tasks]
        schedule_response = ScheduleResponse(
            id=sched.id,
            date=sched.date,
            tasks=tasks_responses,
        )
        schedule_responses.append(schedule_response)

    return schedule_responses


@app.patch("/tasks/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_data: UpdateTask,
    session: Session = Depends(get_session),
    current_user: User = Depends(auth.get_current_user),
):
    db_task = session.get(Task, task_id)
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    if db_task.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed to update this task",
        )
    if task_data.title is not None:
        db_task.title = task_data.title
    if task_data.description is not None:
        db_task.description = task_data.description
    if task_data.priority is not None:
        db_task.priority = task_data.priority
    db_task.updated_at = datetime.utcnow()

    session.commit()
    session.refresh(db_task)

    return TaskResponse(
        id=db_task.id,
        title=db_task.title,
        description=db_task.description,
        priority=db_task.priority,
        status=db_task.status,
        user_id=db_task.user_id,
    )


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(auth.get_current_user),
):
    db_task = session.exec(select(Task).where(Task.id == task_id)).first()
    if not db_task or db_task.user_id != current_user.id:
        raise HTTPException(
            status_code=404, detail="Task not found or not owned by the user"
        )
    session.exec(delete(TaskScheduleLink).where(TaskScheduleLink.task_id == task_id))
    session.delete(db_task)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.patch("/time_analysis/{time_analysis_id}", response_model=TimeAnalysisResponse)
def update_time_analysis(
    time_analysis_id: int,
    time_analysis_data: CreateTimeAnalysis,
    session: Session = Depends(get_session),
    current_user: User = Depends(auth.get_current_user),
):
    time_analysis = session.get(TimeAnalysis, time_analysis_id)
    if not time_analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="TimeAnalysis not found"
        )
    if time_analysis.task.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed to update this TimeAnalysis",
        )

    task = session.get(Task, time_analysis_data.task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )

    if time_analysis_data.time_spent is not None:
        time_analysis.time_spent = time_analysis_data.time_spent

    session.commit()
    session.refresh(time_analysis)

    return TimeAnalysisResponse(
        id=time_analysis.id,
        task_id=time_analysis.task_id,
        time_spent=time_analysis.time_spent,
    )
