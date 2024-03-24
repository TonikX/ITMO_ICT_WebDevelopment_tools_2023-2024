from fastapi import APIRouter, HTTPException
from sqlmodel import select
from fastapi import Depends
from models import BookInstance, BookInstanceBase, BookInstanceReadFull
from db.connection import get_session
from auth.auth import AuthHandler

book_instance_router = APIRouter()
auth_handler = AuthHandler()


@book_instance_router.get("/")
def get_book_instances(session=Depends(get_session)) -> list[BookInstanceReadFull]:
    return session.exec(select(BookInstance)).all()


@book_instance_router.get("/{book_instance_id}")
def get_book_instance(book_instance_id: int, session=Depends(get_session)) -> BookInstanceReadFull:    
    book_instance = session.get(BookInstance, book_instance_id)
    if not book_instance:
        raise HTTPException(status_code=404, detail="Book instance not found")
    return book_instance


@book_instance_router.post("/")
def create_book_instance(book_instance_data: BookInstanceBase, session=Depends(get_session), current=Depends(auth_handler.get_current_user)) -> BookInstance:
    book_instance = BookInstance.model_validate(book_instance_data)
    book_instance.owner_id = current.id
    session.add(book_instance)
    session.commit()
    session.refresh(book_instance)
    return book_instance


@book_instance_router.patch("/{book_instance_id}")
def update_book_instance(book_instance_id: int, book_instance_data: BookInstanceBase, session=Depends(get_session), current=Depends(auth_handler.get_current_user)) -> BookInstance:
    book_instance = session.exec(select(BookInstance).where(BookInstance.id == book_instance_id)).first()
    if not book_instance:
        raise HTTPException(status_code=404, detail="Book not found")
    if book_instance.owner_id != current.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    for key, value in book_instance_data.model_dump(exclude_unset=True).items():
        setattr(book_instance, key, value)
    session.add(book_instance)
    session.commit()
    session.refresh(book_instance)
    return book_instance


@book_instance_router.delete("/{book_instance_id}")
def delete_book_instance(book_instance_id: int, session=Depends(get_session), current=Depends(auth_handler.get_current_user)):
    book_instance = session.exec(select(BookInstance).where(BookInstance.id == book_instance_id)).first()
    if not book_instance:
        raise HTTPException(status_code=404, detail="Book not found")
    if book_instance.owner_id != current.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    session.delete(book_instance)
    session.commit()
    return {"ok": True}