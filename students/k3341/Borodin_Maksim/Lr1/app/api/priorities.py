from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.api.deps import get_current_user
from app.db.session import get_session
from app.models.priority import Priority
from app.models.user import User
from app.schemas.priority import PriorityCreate, PriorityRead, PriorityUpdate

router = APIRouter(prefix="/priorities", tags=["priorities"])


@router.get("", response_model=list[PriorityRead])
def list_priorities(
    session: Session = Depends(get_session),
    _: User = Depends(get_current_user),
) -> list[PriorityRead]:
    items = session.exec(select(Priority).order_by(Priority.weight.desc())).all()
    return [PriorityRead.model_validate(item) for item in items]


@router.get("/{priority_id}", response_model=PriorityRead)
def get_priority(
    priority_id: int,
    session: Session = Depends(get_session),
    _: User = Depends(get_current_user),
) -> PriorityRead:
    item = session.get(Priority, priority_id)
    if not item:
        raise HTTPException(status_code=404, detail="Priority not found")
    return PriorityRead.model_validate(item)


@router.post("", response_model=PriorityRead, status_code=status.HTTP_201_CREATED)
def create_priority(
    payload: PriorityCreate,
    session: Session = Depends(get_session),
    _: User = Depends(get_current_user),
) -> PriorityRead:
    item = Priority.model_validate(payload)
    session.add(item)
    session.commit()
    session.refresh(item)
    return PriorityRead.model_validate(item)


@router.patch("/{priority_id}", response_model=PriorityRead)
def update_priority(
    priority_id: int,
    payload: PriorityUpdate,
    session: Session = Depends(get_session),
    _: User = Depends(get_current_user),
) -> PriorityRead:
    item = session.get(Priority, priority_id)
    if not item:
        raise HTTPException(status_code=404, detail="Priority not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(item, key, value)
    session.add(item)
    session.commit()
    session.refresh(item)
    return PriorityRead.model_validate(item)


@router.delete("/{priority_id}")
def delete_priority(
    priority_id: int,
    session: Session = Depends(get_session),
    _: User = Depends(get_current_user),
) -> dict[str, bool]:
    item = session.get(Priority, priority_id)
    if not item:
        raise HTTPException(status_code=404, detail="Priority not found")
    session.delete(item)
    session.commit()
    return {"ok": True}
