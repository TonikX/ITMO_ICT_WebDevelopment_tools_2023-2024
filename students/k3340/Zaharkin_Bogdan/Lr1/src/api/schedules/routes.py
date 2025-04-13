from fastapi import APIRouter, Depends

from src.api.generic import Response, create_object, delete_object, read_object, read_object_list, update_object
from src.api.schedules.default import ScheduleDefault
from src.api.schedules.schemas import ScheduleInner
from src.db.connection import get_session
from src.db.models import Schedule


router = APIRouter(prefix="/schedules", tags=["schedules"])


# CRUD for Schedule
@router.post("/")
def create_schedule(schedule: ScheduleDefault, session=Depends(get_session)) -> Response[Schedule]:
    """
    Create a new schedule.

    - **schedule**: ScheduleDefault object containing schedule details.
    - **session**: Database session dependency.

    Returns:
        Response[Schedule]: The created schedule.
    """
    return create_object(session, schedule, Schedule)

@router.get("/")
def get_schedules(session=Depends(get_session)) -> list[Schedule]:
    """
    Get a list of all schedules.

    - **session**: Database session dependency.

    Returns:
        list[Schedule]: List of schedules.
    """
    return read_object_list(session, Schedule)

@router.get("/{schedule_id}", response_model=ScheduleInner)
def get_schedule(schedule_id: int, session=Depends(get_session)) -> Schedule:
    """
    Get a schedule by ID.

    - **schedule_id**: ID of the schedule to retrieve.
    - **session**: Database session dependency.

    Returns:
        Schedule: The schedule with the specified ID.
    """
    return read_object(session, schedule_id, Schedule)

@router.patch("/{schedule_id}")
def update_schedule(schedule_id: int, schedule: ScheduleDefault, session=Depends(get_session)) -> ScheduleDefault:
    """
    Update a schedule by ID.

    - **schedule_id**: ID of the schedule to update.
    - **schedule**: ScheduleDefault object containing updated schedule details.
    - **session**: Database session dependency.

    Returns:
        ScheduleDefault: The updated schedule.
    """
    return update_object(session, schedule_id, schedule, Schedule)

@router.delete("/{schedule_id}")
def delete_schedule(schedule_id: int, session=Depends(get_session)) -> dict:
    """
    Delete a schedule by ID.

    - **schedule_id**: ID of the schedule to delete.
    - **session**: Database session dependency.

    Returns:
        dict: A dictionary indicating the result of the deletion.
    """
    return delete_object(session, schedule_id, Schedule)
