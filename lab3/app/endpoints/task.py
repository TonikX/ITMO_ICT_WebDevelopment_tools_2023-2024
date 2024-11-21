from datetime import datetime, date
from typing import List, Optional
from fastapi import HTTPException, Depends, APIRouter
from sqlmodel import select, Session
from typing_extensions import TypedDict
from models import Task, TaskDefault, TaskTime, StatusEnum, PriorityEnum, TagDefault, Tag
from connection import get_session

router = APIRouter()


@router.get("/", response_model=List[Task])
def tasks_list(session=Depends(get_session)) -> List[Task]:
    return session.exec(select(Task)).all()


@router.get("/{task_id}", response_model=Task)
def get_task(task_id: int, session=Depends(get_session)) -> Task:
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.post("/")
def create_task(
        task_data: TaskDefault,
        tag_data: List[TagDefault] = None,
        session=Depends(get_session)
) -> TypedDict('Response', {"status": int, "data": Task, "tag_data": List}):
    # Инициализируем тегов, если их нет
    if tag_data is None:
        tag_data = []

    # Создаем объект задачи из предоставленных данных
    task = Task(**task_data.dict())
    session.add(task)
    session.flush()  # Сохраняем задачу, чтобы получить ее ID

    # Обработка тегов
    for tag_info in tag_data:
        if tag_info.name:  # Проверяем, что имя тега не пустое
            existing_tag = session.exec(select(Tag).where(Tag.name == tag_info.name)).first()
            if existing_tag:
                task.tags.append(existing_tag)  # Добавляем существующий тег
            else:
                new_tag = Tag(**tag_info.dict())
                session.add(new_tag)
                session.flush()  # Сохраняем новый тег
                task.tags.append(new_tag)  # Добавляем новый тег к задаче

    session.commit()  # Сохраняем все изменения
    session.refresh(task)  # Обновляем объект задачи с новыми данными

    return {"status": 200, "data": task, "tag_data": [tag_info.dict() for tag_info in tag_data]}


@router.patch("/{task_id}/add_tags")
def add_tags_to_task(
        task_id: int,
        tag_data: List[TagDefault],
        session=Depends(get_session)
) -> TypedDict('Response', {"message": str}):
    task = session.get(Task, task_id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Обработка тегов
    for tag_info in tag_data:
        if tag_info.name:  # Проверяем, что имя тега не пустое
            existing_tag = session.exec(select(Tag).where(Tag.name == tag_info.name)).first()
            if existing_tag:
                task.tags.append(existing_tag)  # Добавляем существующий тег
            else:
                new_tag = Tag(**tag_info.dict())
                session.add(new_tag)
                session.flush()  # Сохраняем новый тег
                task.tags.append(new_tag)  # Добавляем новый тег к задаче
        else:
            raise HTTPException(status_code=400, detail="Tag name cannot be empty")

    session.commit()  # Сохраняем изменения

    return {"message": "Tags added to task successfully"}


@router.patch("/{task_id}/start_task")
def start_task(task_id: int, session=Depends(get_session)) -> TypedDict('Response', {"message": str}):
    task = session.get(Task, task_id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Если task_time не инициализирован, создайте новый объект TaskTime
    if task.task_time is None:
        task.task_time = TaskTime()  # Инициализация нового объекта TaskTime

    task.task_time.start_time = datetime.now()
    task.status = StatusEnum.in_progress
    session.commit()

    return {"message": "Task start time and status updated successfully"}


@router.patch("/{task_id}/finish_task")
def finish_task(task_id: int, session=Depends(get_session)) -> TypedDict('Response', {"message": str}):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.task_time.end_time = datetime.now()
    task.status = StatusEnum.done
    session.commit()

    return {"message": "Task finished successfully"}


@router.patch("/{task_id}/time_spent")
def get_task_time(task_id: int, session=Depends(get_session)) -> TypedDict('Response', {"task_id": int, "total_time_spent": str}):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Проверяем, инициализирован ли task_time
    if task.task_time is None or task.task_time.start_time is None or task.task_time.end_time is None:
        raise HTTPException(status_code=400, detail="Task has not been started or finished yet")

    # Вычисляем общее время, потраченное на задачу
    total_time_spent = task.task_time.end_time - task.task_time.start_time

    return {"task_id": task_id, "total_time_spent": str(total_time_spent)}


@router.delete("/{task_id}")
def delete_task(task_id: int, session=Depends(get_session)) -> TypedDict('Response', {"is_deleted": bool}):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    session.delete(task)
    session.commit()
    return {"is_deleted": True}


@router.patch("/{task_id}")
def update_task(
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        deadline: Optional[date] = None,
        priority: Optional[PriorityEnum] = None,
        category_id: Optional[int] = None,
        session: Session = Depends(get_session)
) -> TypedDict('Response', {"title": str, "description": str, "deadline": date, "priority": PriorityEnum,
                            "category_id": Optional[int]}):
    task = session.get(Task, task_id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    update_data = {
        "title": title,
        "description": description,
        "deadline": deadline,
        "priority": priority,
        "category_id": category_id
    }

    for field, value in update_data.items():
        if value is not None:
            setattr(task, field, value)

    session.commit()

    return {
        "title": task.title,
        "description": task.description,
        "deadline": task.deadline,
        "priority": task.priority,
        "category_id": task.category_id
    }
