from fastapi import APIRouter, Depends

from src.api.generic import Response, read_object_list
from src.api.schedule_tasks.schedule_tasks import create_st, delete_st, get_st
from src.db.connection import get_session
from src.db.models import ScheduleTask


router = APIRouter(prefix="/schedule_tasks", tags=["schedule_tasks"])


# CRUD for ScheduleTask
@router.post("/{schedule_id}/{task_id}")
def create_schedule_task(schedule_id: int, task_id: int, session=Depends(get_session)) -> Response[ScheduleTask]:
    """
    Create a new schedule task.

    - **schedule_id**: ID of the schedule.
    - **task_id**: ID of the task.
    - **session**: Database session dependency.

    Returns:
        Response[ScheduleTask]: The created schedule task.
    """
    return create_st(schedule_id, task_id, session)

@router.get("/")
def get_schedule_tasks(session=Depends(get_session)) -> list[ScheduleTask]:
    """
    Get a list of all schedule tasks.

    - **session**: Database session dependency.

    Returns:
        list[ScheduleTask]: List of schedule tasks.
    """
    return read_object_list(session, ScheduleTask)

@router.get("/{schedule_id}/{task_id}")
def get_schedule_task(schedule_id: int, task_id: int, session=Depends(get_session)) -> ScheduleTask:
    """
    Get a schedule task by schedule ID and task ID.

    - **schedule_id**: ID of the schedule.
    - **task_id**: ID of the task.
    - **session**: Database session dependency.

    Returns:
        ScheduleTask: The schedule task with the specified IDs.
    """
    return get_st(schedule_id, task_id, session)

@router.delete("/{schedule_id}/{task_id}")
def delete_schedule_task(schedule_id: int, task_id: int, session=Depends(get_session)) -> dict:
    """
    Delete a schedule task by schedule ID and task ID.

    - **schedule_id**: ID of the schedule.
    - **task_id**: ID of the task.
    - **session**: Database session dependency.

    Returns:
        dict: A dictionary indicating the result of the deletion.
    """
    return delete_st(schedule_id, task_id, session)
