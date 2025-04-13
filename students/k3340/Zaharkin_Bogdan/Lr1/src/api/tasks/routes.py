from fastapi import APIRouter, Depends

from src.api.generic import Response, create_object, delete_object, read_object, read_object_list, update_object
from src.api.tasks.default import TaskDefault
from src.api.tasks.schemas import TaskInner
from src.db.connection import get_session
from src.db.models import Task


router = APIRouter(prefix="/tasks", tags=["tasks"])


# CRUD for Task
@router.post("/")
def create_task(task: TaskDefault, session=Depends(get_session)) -> Response[Task]:
    """
    Create a new task.

    - **task**: TaskDefault object containing task details.
    - **session**: Database session dependency.

    Returns:
        Response[Task]: The created task.
    """
    return create_object(session, task, Task)

@router.get("/")
def get_tasks(session=Depends(get_session)) -> list[Task]:
    """
    Get a list of all tasks.

    - **session**: Database session dependency.

    Returns:
        list[Task]: List of tasks.
    """
    return read_object_list(session, Task)

@router.get("/{task_id}", response_model=TaskInner)
def get_task(task_id: int, session=Depends(get_session)) -> Task:
    """
    Get a task by ID.

    - **task_id**: ID of the task to retrieve.
    - **session**: Database session dependency.

    Returns:
        Task: The task with the specified ID.
    """
    return read_object(session, task_id, Task)

@router.patch("/{task_id}")
def update_task(task_id: int, task: TaskDefault, session=Depends(get_session)) -> TaskDefault:
    """
    Update a task by ID.

    - **task_id**: ID of the task to update.
    - **task**: TaskDefault object containing updated task details.
    - **session**: Database session dependency.

    Returns:
        TaskDefault: The updated task.
    """
    return update_object(session, task_id, task, Task)

@router.delete("/{task_id}")
def delete_task(task_id: int, session=Depends(get_session)) -> dict:
    """
    Delete a task by ID.

    - **task_id**: ID of the task to delete.
    - **session**: Database session dependency.

    Returns:
        dict: A dictionary indicating the result of the deletion.
    """
    return delete_object(session, task_id, Task)
