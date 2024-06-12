from fastapi import Depends, FastAPI, HTTPException, APIRouter
from sqlmodel import select, Session
from datetime import datetime

from db.models import RequestDefault, Request, AppUser, Book, StatusType
from connection import get_session
from .auth import get_current_user

router = APIRouter()


@router.get("/my", response_model=list[Request])
def get_requests(session: Session = Depends(get_session), current_user: AppUser = Depends(get_current_user)):
    current_user_books = session.exec(select(Book).where(Book.user_id == current_user.id)).all()
    book_ids = [book.id for book in current_user_books]

    # Filter the requests where the current user's books are involved
    requests = session.exec(
        select(Request)
        .where((Request.requester_book_id.in_(book_ids)) | (Request.recipient_book_id.in_(book_ids)))
    ).all()
    return requests

@router.get("/{request_id}/my", response_model=Request)
def get_request(request_id: int, session: Session = Depends(get_session), current_user: AppUser = Depends(get_current_user)):
    request = session.get(Request, request_id)
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")
    
    # Check if the current user is the owner of the requester_book or recipient_book
    requester_book = session.get(Book, request.requester_book_id)
    recipient_book = session.get(Book, request.recipient_book_id)
    if requester_book.user_id != current_user.id and recipient_book.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not authorized to view this request")
    
    return request

@router.post("/", response_model=Request)
def create_request(request: RequestDefault, session: Session = Depends(get_session), current_user: AppUser = Depends(get_current_user)):
    requester_book = session.get(Book, request.requester_book_id)
    if requester_book is None or requester_book.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Requester book not found")
    if session.get(Book, request.recipient_book_id) is None:
        raise HTTPException(status_code=404, detail="Recipient book not found")

    db_request = Request(
        requester_book_id=request.requester_book_id,
        recipient_book_id=request.recipient_book_id,
        message=request.message,
        status=request.status,
    )

    session.add(db_request)
    session.commit()
    return db_request

@router.put("/{request_id}/status", response_model=Request)
def update_request(request_id: int, new_status: StatusType, session: Session = Depends(get_session), current_user: AppUser = Depends(get_current_user)):
    db_request = session.get(Request, request_id)
    if not db_request:
        raise HTTPException(status_code=404, detail="Request not found")
    
    # Check if the current user is the owner of the requester_book or recipient_book
    requester_book = session.get(Book, db_request.requester_book_id)
    recipient_book = session.get(Book, db_request.recipient_book_id)
    if requester_book.user_id != current_user.id and recipient_book.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Permission denied")
    
    # Update the request's attributes
    db_request.status = new_status.name
    db_request.last_updated_at = datetime.now()

    session.add(db_request)
    session.commit()
    return db_request

@router.delete("/{request_id}")
def delete_request(request_id: int, session: Session = Depends(get_session), current_user: AppUser = Depends(get_current_user)):
    db_request = session.get(Request, request_id)
    if not db_request:
        raise HTTPException(status_code=404, detail="Request not found")
    
    # Check if the current user is the owner of the requester_book
    requester_book = session.get(Book, db_request.requester_book_id)
    if requester_book.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not authorized to delete this request")
    
    session.delete(db_request)
    session.commit()
    return {"message": "Request deleted"}