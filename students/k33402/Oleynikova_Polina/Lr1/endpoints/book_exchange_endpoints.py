from fastapi import APIRouter, HTTPException
from sqlmodel import select
from fastapi import Depends
from models import BookExchange, BookExchangeBase, BookExchangeChangeStatus, BookExchangeReadFull
from db.connection import get_session
from auth.auth import AuthHandler
from models import BookInstance

book_exchange_router = APIRouter()
auth_handler = AuthHandler()


@book_exchange_router.get("/sender")
def get_book_exchanges(session=Depends(get_session), current=Depends(auth_handler.get_current_user)) -> list[BookExchangeReadFull]:
    return session.exec(select(BookExchange).where(BookExchange.sender_id==current.id)).all()


@book_exchange_router.get("/receiver")
def get_book_exchanges(session=Depends(get_session), current=Depends(auth_handler.get_current_user)) -> list[BookExchangeReadFull]:
    return session.exec(select(BookExchange).where(BookExchange.receiver_id==current.id)).all()


@book_exchange_router.get("/{book_exchange_id}")
def get_book_exchange(book_exchange_id: int, session=Depends(get_session)) -> BookExchangeReadFull:    
    book_exchange = session.get(BookExchange, book_exchange_id)
    if not book_exchange:
        raise HTTPException(status_code=404, detail="Book exchange not found")
    return book_exchange


@book_exchange_router.post("/")
def create_book_exchange(book_exchange_data: BookExchangeBase, session=Depends(get_session), current=Depends(auth_handler.get_current_user)) -> BookExchange:
    book_exchange = BookExchange.model_validate(book_exchange_data)
    book_instance = session.get(BookInstance, book_exchange_data.book_instance_id)
    book_exchange.receiver_id = current.id
    book_exchange.sender_id = book_instance.owner_id
    session.add(book_exchange)
    session.commit()
    session.refresh(book_exchange)
    return book_exchange


@book_exchange_router.patch("/{book_exchange_id}")
def update_book_exchange(book_exchange_id: int, book_exchange_data: BookExchangeChangeStatus, session=Depends(get_session), current=Depends(auth_handler.get_current_user)) -> BookExchange:
    book_exchange = session.exec(select(BookExchange).where(BookExchange.id == book_exchange_id)).first()
    if not book_exchange:
        raise HTTPException(status_code=404, detail="Book exchange not found")
    if book_exchange.sender_id!=current.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    book_exchange.status = book_exchange_data.status
    session.add(book_exchange)
    session.commit()
    session.refresh(book_exchange)
    return book_exchange


@book_exchange_router.delete("/{book_exchange_id}")
def delete_book_exchange(book_exchange_id: int, session=Depends(get_session), current=Depends(auth_handler.get_current_user)):
    book_exchange = session.exec(select(BookExchange).where(BookExchange.id == book_exchange_id)).first()
    if not book_exchange:
        raise HTTPException(status_code=404, detail="Book exchange not found")
    if book_exchange.receiver_id!=current.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    session.delete(book_exchange)
    session.commit()
    return {"ok": True}