from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import delete, select
from connection import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import TypedDict
from base_responses import MessageResponse
from typing import List, Optional
from pydantic import BaseModel
from auth_services import get_current_user
from models import Task, TaskCategory, TaskDefault, TaskTimeLogDefault,TaskTimeLog, Priority, User, Category
from sqlalchemy.orm import selectinload
import pytz
tz = pytz.UTC

class TaskModel(TaskDefault):
    id: int
    priority: Priority
    categories: List[Category] = None
    time_logs: List[TaskTimeLog] = None

class TaskCreate(TaskDefault):
    category_ids: Optional[List[int]] = []

class TaskResponse(TypedDict):
    status: int
    data: TaskModel

class TaskListResponse(TypedDict):
    status: int
    data: List[TaskModel]

router = APIRouter()

@router.post("/", response_model=TaskResponse)
async def create_task(task_data: TaskCreate, 
                      current_user: User = Depends(get_current_user),
                      session: AsyncSession = Depends(get_session)) -> TaskResponse:
    if task_data.due_date and task_data.due_date.tzinfo is None:
        task_data.due_date = task_data.due_date.replace(tzinfo=tz)

    if task_data.scheduled_datetime and task_data.scheduled_datetime.tzinfo is None:
        task_data.scheduled_datetime = task_data.scheduled_datetime.replace(tzinfo=tz)

    task = Task(**task_data.model_dump(), user_id=current_user.id)
    session.add(task)
    await session.commit()
    await session.refresh(task)

    if task_data.category_ids:
        categories_result = await session.execute(
            select(Category).where(Category.id.in_(task_data.category_ids))
        )
        categories = categories_result.scalars().all()
        for category in categories:
            task_category = TaskCategory(task_id=task.id, category_id=category.id)
            session.add(task_category)
    await session.commit()

    result = await session.execute(
        select(Task)
        .options(selectinload(Task.user), selectinload(Task.categories), selectinload(Task.time_logs))
        .where(Task.id == task.id)
    )
    task_with_relations = result.scalars().first()
    task_with_relations_dict = TaskModel.model_validate(task_with_relations)

    if task_with_relations_dict:
        return {"status": 200, "data": task_with_relations_dict}
    else:
        raise HTTPException(status_code=404, detail="Task not found")


@router.get("/", response_model=TaskListResponse)
async def get_all_tasks(current_user: User = Depends(get_current_user), 
                        session: AsyncSession = Depends(get_session)) -> TaskListResponse:
    result = await session.execute(
        select(Task)
        .where(Task.user_id == current_user.id)
        .options(selectinload(Task.categories), selectinload(Task.time_logs))
    )
    tasks = result.scalars().all()
    return {"status": 200, "data": [TaskModel.model_validate(task) for task in tasks]}


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(task_id: int, 
                   current_user: User = Depends(get_current_user),
                   session: AsyncSession = Depends(get_session)) -> TaskResponse:
    result = await session.execute(
        select(Task)
        .options(selectinload(Task.categories), selectinload(Task.time_logs))
        .where(Task.id == task_id and Task.user_id == current_user.id)
    )
    task = result.scalars().first()
    if task:
        return {"status": 200, "data": TaskModel.model_validate(task)}
    else:
        raise HTTPException(status_code=404, detail="Task not found")
    

@router.put("/{task_id}")
async def update_task(task_id: int, 
                      task_data: TaskCreate, 
                      current_user: User = Depends(get_current_user),
                      session: AsyncSession = Depends(get_session)) -> MessageResponse:
    result = await session.execute(select(Task).where(Task.id == task_id and Task.user_id == current_user.id))
    task = result.scalars().first()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Обновление полей задачи
    if task_data.due_date:
        task.due_date = task_data.due_date.replace(tzinfo=tz) if task_data.due_date.tzinfo is None else task_data.due_date
    if task_data.scheduled_datetime:
        task.scheduled_datetime = task_data.scheduled_datetime.replace(tzinfo=tz) if task_data.scheduled_datetime.tzinfo is None else task_data.scheduled_datetime
    if task_data.title:
        task.title = task_data.title
    if task_data.description:
        task.description = task_data.description
    if task_data.priority:
        task.priority = task_data.priority

    # Обработка категорий (если они переданы)
    if task_data.category_ids is not None:
        await session.execute(
            delete(TaskCategory).where(TaskCategory.task_id == task.id)
        )
        await session.commit()

        if task_data.category_ids:
            categories_result = await session.execute(
                select(Category).where(Category.id.in_(task_data.category_ids))
            )
            categories = categories_result.scalars().all()
            for category in categories:
                task_category = TaskCategory(task_id=task.id, category_id=category.id)
                session.add(task_category)

    await session.commit()
    await session.refresh(task)

    return {"status": 200, "message": "Task updated successfully"}

@router.delete("/{task_id}")
async def delete_task(task_id: int, 
                      current_user: User = Depends(get_current_user),
                      session: AsyncSession = Depends(get_session)) -> MessageResponse:
    result = await session.execute(select(Task).where(Task.id == task_id and Task.user_id == current_user.id))
    task = result.scalars().first()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Удаляем связи с категориями
    await session.execute(
        delete(TaskCategory).where(TaskCategory.task_id == task.id)
    )
    await session.commit()

    await session.delete(task)
    await session.commit()

    return {"status": 200, "message": "Task deleted successfully"}


class TaskTimeLogResponse(BaseModel):
    status: int
    data: TaskTimeLog

@router.post("/{task_id}/time_logs", response_model=TaskTimeLogResponse)
async def add_time_log(task_id: int, 
                       time_log_data: TaskTimeLogDefault, 
                       current_user: User = Depends(get_current_user),
                       session: AsyncSession = Depends(get_session)) -> TaskTimeLogResponse:

    result = await session.execute(select(Task).where(Task.id == task_id and Task.user_id == current_user.id))
    task = result.scalars().first()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if time_log_data.start_time.tzinfo is None:
        time_log_data.start_time = tz.localize(time_log_data.start_time)
    if time_log_data.end_time.tzinfo is None:
        time_log_data.end_time = tz.localize(time_log_data.end_time)

    time_log = TaskTimeLog(
        task_id=task.id,
        start_time = time_log_data.start_time,
        end_time = time_log_data.end_time,
        time_spent=(time_log_data.end_time - time_log_data.start_time).total_seconds()
    )
    
    session.add(time_log)
    await session.commit()
    await session.refresh(time_log)

    return {"status": 200, "data": time_log}

@router.put("/{task_id}/time_logs/{time_log_id}", response_model=TaskTimeLogResponse)
async def update_time_log(
    task_id: int, 
    time_log_id: int, 
    time_log_data: TaskTimeLogDefault, 
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
) -> TaskTimeLogResponse:
    result = await session.execute(select(Task).where(Task.id == task_id and Task.user_id == current_user.id))
    task = result.scalars().first()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    time_log_result = await session.execute(select(TaskTimeLog).where(TaskTimeLog.id == time_log_id, TaskTimeLog.task_id == task_id))
    time_log = time_log_result.scalars().first()

    if not time_log:
        raise HTTPException(status_code=404, detail="Time log not found")
    
    if time_log_data.start_time.tzinfo is None:
        time_log_data.start_time = tz.localize(time_log_data.start_time)
    if time_log_data.end_time.tzinfo is None:
        time_log_data.end_time = tz.localize(time_log_data.end_time)
    
    if time_log_data.start_time:
        time_log.start_time = time_log_data.start_time
    if time_log_data.end_time:
        time_log.end_time = time_log_data.end_time
    time_log.time_spent = (time_log_data.end_time - time_log_data.start_time).total_seconds()

    await session.commit()
    await session.refresh(time_log)

    return {"status": 200, "data": time_log}


@router.delete("/{task_id}/time_logs/{time_log_id}")
async def delete_time_log(task_id: int, 
                          time_log_id: int, 
                          current_user: User = Depends(get_current_user),
                          session: AsyncSession = Depends(get_session)) -> MessageResponse:
    result = await session.execute(select(Task).where(Task.id == task_id and Task.user_id == current_user.id))
    task = result.scalars().first()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    time_log_result = await session.execute(select(TaskTimeLog).where(TaskTimeLog.id == time_log_id, TaskTimeLog.task_id == task_id))
    time_log = time_log_result.scalars().first()

    if not time_log:
        raise HTTPException(status_code=404, detail="Time log not found")
    
    await session.delete(time_log)
    await session.commit()

    return {"status": 200, "message": "Time log deleted successfully"}