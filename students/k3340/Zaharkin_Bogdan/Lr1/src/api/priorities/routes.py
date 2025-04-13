from fastapi import APIRouter, Depends

from src.api.generic import Response, create_object, delete_object, read_object, read_object_list, update_object
from src.api.priorities.default import PriorityDefault
from src.api.priorities.schemas import PriorityInner
from src.db.connection import get_session
from src.db.models import Priority


router = APIRouter(prefix="/priorities", tags=["priorities"])


# CRUD for Priority
@router.post("/")
def create_priority(priority: PriorityDefault, session=Depends(get_session)) -> Response[Priority]:
    """
    Create a new priority.

    - **priority**: PriorityDefault object containing priority details.
    - **session**: Database session dependency.

    Returns:
        Response[Priority]: The created priority.
    """
    return create_object(session, priority, Priority)

@router.get("/")
def get_priorities(session=Depends(get_session)) -> list[Priority]:
    """
    Get a list of all priorities.

    - **session**: Database session dependency.

    Returns:
        list[Priority]: List of priorities.
    """
    return read_object_list(session, Priority)

@router.get("/{priority_id}", response_model=PriorityInner)
def get_priority(priority_id: int, session=Depends(get_session)) -> Priority:
    """
    Get a priority by ID.

    - **priority_id**: ID of the priority to retrieve.
    - **session**: Database session dependency.

    Returns:
        Priority: The priority with the specified ID.
    """
    return read_object(session, priority_id, Priority)

@router.patch("/{priority_id}")
def update_priority(priority_id: int, priority: PriorityDefault, session=Depends(get_session)) -> PriorityDefault:
    """
    Update a priority by ID.

    - **priority_id**: ID of the priority to update.
    - **priority**: PriorityDefault object containing updated priority details.
    - **session**: Database session dependency.

    Returns:
        PriorityDefault: The updated priority.
    """
    return update_object(session, priority_id, priority, Priority)

@router.delete("/{priority_id}")
def delete_priority(priority_id: int, session=Depends(get_session)) -> dict:
    """
    Delete a priority by ID.

    - **priority_id**: ID of the priority to delete.
    - **session**: Database session dependency.

    Returns:
        dict: A dictionary indicating the result of the deletion.
    """
    return delete_object(session, priority_id, Priority)
