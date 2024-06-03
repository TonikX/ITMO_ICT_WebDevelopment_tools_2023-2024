from typing import List

from fastapi import HTTPException, Depends, APIRouter
from sqlmodel import select, Session

from connection import get_session
from models import BookCopy, Sharing, SharingStatus

router = APIRouter(prefix="/sharing", tags=["Sharing"])


@router.post("/take/{user_id}", response_model=Sharing)
def take_book(user_id: int, book_copy_id: int, session: Session = Depends(get_session)):
    active_sharings = session.exec(
        select(Sharing)
        .where(Sharing.book_copy_id == book_copy_id)
        .where(Sharing.status == SharingStatus.active)
    )
    print(len(active_sharings.all()))
    if len(active_sharings.all()) != 0:
        raise HTTPException(status_code=409, detail=f"You cant take book {book_copy_id} now, its already in use")
    book_copy = session.get(BookCopy, book_copy_id)
    if not book_copy:
        raise HTTPException(status_code=404, detail=f"Book copy {book_copy_id} not found")
    sharing = Sharing(taking_id=user_id, book_copy_id=book_copy_id, owner_id=book_copy.user_id)
    session.add(sharing)
    session.commit()
    session.refresh(sharing)
    return sharing


@router.get("/take/{user_id}", response_model=List[Sharing])
def show_active_sharings(user_id: int, session: Session = Depends(get_session)):
    active_sharings = session.exec(
        select(Sharing)
        .where(Sharing.taking_id == user_id)
    )
    return active_sharings


@router.delete("take/{user_id}", response_model=dict)
def delete_sharing(sharing_id: int, session: Session = Depends(get_session)):
    sharing = session.get(Sharing, sharing_id)
    if not sharing:
        raise HTTPException(status_code=404, detail="Sharing not found")
    session.delete(sharing)
    session.commit()
    return {"message": "Sharing deleted successfully"}


@router.patch("/take/{sharing_id}", response_model=Sharing)
def create_book_copy(sharing_id: int, status: SharingStatus, session=Depends(get_session)):
    sharing = session.get(Sharing, sharing_id)
    if not sharing:
        raise HTTPException(status_code=404, detail="Sharing not found")
    setattr(sharing, "status", status)
    session.add(sharing)
    session.commit()
    session.refresh(sharing)
    return sharing
