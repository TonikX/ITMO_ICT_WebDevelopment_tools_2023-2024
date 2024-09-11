from fastapi import APIRouter, HTTPException
from fastapi import Depends, status
from schemas import Task, TaskDefault, TaskDisplay
from database import get_session
from typing_extensions import TypedDict

router = APIRouter(tags=["Task"])

@router.post("/task-create", status_code=status.HTTP_201_CREATED)
def task_create(task: TaskDefault, session=Depends(get_session)) -> Task:
    task = Task.model_validate(task)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@router.get("/list-tasks", status_code=status.HTTP_200_OK)
def tasks_list(session=Depends(get_session)) -> list[Task]:
    return session.query(Task).all()


@router.get("/task/{task_id}", status_code=status.HTTP_200_OK, response_model=TaskDisplay)
def task_get(task_id: int, session=Depends(get_session)) -> Task:
    obj = session.get(Task, task_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="task not found")
    return obj


@router.patch("/task/update/{task_id}", status_code=status.HTTP_202_ACCEPTED)
def task_update(task_id: int, task: TaskDefault, session=Depends(get_session)) \
        -> Task:
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


@router.delete("/task/delete/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def task_delete(task_id: int, session=Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="task not found")
    session.delete(task)
    session.commit()
    return {"ok": True}

