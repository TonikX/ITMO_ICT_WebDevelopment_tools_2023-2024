# Задачи
## Эндпоинты для задач

Были реализованы следующие эндпоинты:

* получение списка задач;
* получение задачи по id;
* создание задачи;
* удаление задачи;
* изменение задачи;
* добавление тегов задачи;
* начало задачи;
* заверешение задачи;
* пауза задачи;
* получение времени выполнения задачи.


Код реализации:

    
    from datetime import datetime, date
    from typing import List, Optional
    from fastapi import HTTPException, Depends, APIRouter
    from sqlmodel import select, Session
    from typing_extensions import TypedDict
    from models import TasksDetails, Task, LabelDefault, Label, TaskDefault, StatusEnum, PriorityEnum
    from connection import get_session
    
    
    router = APIRouter()
    
    
    @router.get("", response_model=List[TasksDetails])
    def tasks_list(session=Depends(get_session)) -> List[Task]:
        return session.exec(select(Task)).all()
    
    
    @router.get("/{task_id}", response_model=TasksDetails)
    def get_task(task_id: int, session=Depends(get_session)) -> Task:
        task = session.get(Task, task_id)
        return task
    
    
    @router.post("/")
    def create_task(task_data: TaskDefault, label_data: List[LabelDefault] = None,
                    session=Depends(get_session)) -> TypedDict('Response', {"status": int, "data": Task,
                                                                            "label_data": List}):
        if label_data is None:
            label_data = []
    
        task = Task(**task_data.dict())
        session.add(task)
        session.flush()
    
        for label_info in label_data:
            if label_info.content:
                existing_label = session.exec(select(Label).where(Label.content == label_info.content)).first()
                if existing_label:
                    task.labels.append(existing_label)
                else:
                    label = Label(**label_info.dict())
                    session.add(label)
                    session.flush()
                    task.labels.append(label)
    
        session.commit()
        session.refresh(task)
        return {"status": 200, "data": task, "label_data": [label_info.dict() for label_info in label_data]}
    
    
    @router.patch("/{task_id}/add_labels")
    def add_labels_to_task(task_id: int, label_data: List[LabelDefault], session=Depends(get_session)) \
            -> TypedDict('Response', {"message": str}):
        task = session.get(Task, task_id)
    
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
    
        for label_info in label_data:
            if label_info.content:
                label = Label(**label_info.dict())
                session.add(label)
                session.flush()
                task.labels.append(label)
            else:
                raise HTTPException(status_code=500, detail="Empty content")
    
        session.commit()
    
        return {"message": "Labels added to task successfully"}
    
    
    @router.patch("/{task_id}/start_task")
    def start_task(task_id: int, session=Depends(get_session)) -> TypedDict('Response', {"message": str}):
        task = session.get(Task, task_id)
    
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
    
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
    
    
    @router.patch("/{task_id}/stop_task")
    def stop_task(task_id: int, session=Depends(get_session)) -> TypedDict('Response', {"message": str}):
        task = session.get(Task, task_id)
    
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
    
        task.task_time.start_time = datetime.now()
        task.status = StatusEnum.to_do
        session.commit()
    
        return {"message": "Task stopped successfully"}
    
    
    @router.patch("/{task_id}/time_spent")
    def get_task_time(task_id: int, session=Depends(get_session))\
            -> TypedDict('Response', {"task_id": int, "total_time_spent": float}):
        task = session.get(Task, task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        total_time_spent = task.task_time.end_time - task.task_time.start_time
        return {"task_id": task_id, "total_time_spent": total_time_spent}
    
    
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
                                "category_id": int | None}):
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
