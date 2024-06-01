from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from connection import get_session
from schemas import *
import crud

router = APIRouter()

@router.post("/tasks/",
        response_model=Task,
        status_code=status.HTTP_201_CREATED,
        tags=["Tasks"],  # Теги для организации в документации
        summary="Create a new task",  # Краткое описание метода
        description="Create a new task with the provided data.",
        responses={  # Примеры ответов
            201: {"description": "Task created successfully"},
            400: {"description": "Invalid data provided"},
            500: {"description": "Internal server error"},
    })
def create_task(task_data: TaskCreate, db: Session = Depends(get_session)):
    return crud.create_task(db=db, **task_data.dict())

@router.get("/tasks/{task_id}", response_model=Task)
def read_task(task_id: int, db: Session = Depends(get_session)):
    db_task = crud.get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@router.get("/tasks/", response_model=TaskList)
def read_all_tasks(db: Session = Depends(get_session)):
    tasks = crud.get_all_tasks(db)
    return {"tasks": tasks}

@router.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task_data: TaskUpdate, db: Session = Depends(get_session)):
    db_task = crud.get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return crud.update_task(db=db, task_id=task_id, **task_data.dict(exclude_unset=True))

@router.delete("/tasks/{task_id}", response_model=Task)
def delete_task(task_id: int, db: Session = Depends(get_session)):
    db_task = crud.get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return crud.delete_task(db=db, task_id=task_id)

@router.get("/tasks/user/{user_id}", response_model=TaskList)
def read_user_tasks(user_id: int, db: Session = Depends(get_session)):
    tasks = crud.get_user_tasks(db, user_id)
    if not tasks:
        raise HTTPException(status_code=404, detail="User has no tasks")
    return {"tasks": tasks}

@router.get("/tasks/{task_id}/user", response_model=UserRead)
def read_user_by_task_id(task_id: int, db: Session = Depends(get_session)):
    user = crud.get_user_by_task_id(db, task_id)
    if not user:
        raise HTTPException(status_code=404, detail="Task not found")
    return user

@router.get("/tasks-with-time-logs/{task_id}", response_model=TaskWithTimeLogsList)
def read_tasks_with_time_logs(task_id: int, db: Session = Depends(get_session)):
    tasks = crud.get_tasks_with_time_logs(db, task_id)
    if not tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"tasks": tasks}

@router.post("/tasks/{task_id}/add-time-log")
def add_time_log_to_task(task_id: int, time_spent_minutes: int, date_logged: date, db: Session = Depends(get_session)):
    return crud.add_time_log(db, task_id, time_spent_minutes, date_logged)

@router.get("/tasks/{task_id}/time-logs")
def get_time_logs_for_task(task_id: int, db: Session = Depends(get_session)):
    return crud.get_time_logs_for_task(db, task_id)

@router.post("/parse/", response_model=TaskListParse)
async def parse_and_save_to_db_endpoint(start_page: int, end_page: int, db: Session = Depends(get_session)):
    parsed_data = await crud.parse_and_save_to_db(start_page, end_page)
    return {"tasks": parsed_data}
