from typing import Annotated
from typing_extensions import TypedDict
from fastapi import APIRouter, Depends

from app.services import Monolite
from app.depends import get_monolite_server

from app.model import (

    BookDefault,
    BookUpdate,
    Book,

    ExchangeCreate,
    Exchange,
    BooksChange,
    
    ResponseExchangeBook,
)

app_router = APIRouter()

#Book


@app_router.get("/books_list", tags=["Книга"])
async def books_list(server: Annotated[Monolite, Depends(get_monolite_server)]) -> list[Book]:
    return await server.get_book_list()


@app_router.get("/book/{book_id}", tags=["Книга"])
async def get_books(book_id: int, server: Annotated[Monolite, Depends(get_monolite_server)]) -> Book:
    return await server.get_book(book_id)


@app_router.post("/book", tags=["Книга"])
async def books_create(book: BookDefault, server: Annotated[Monolite, Depends(get_monolite_server)]) -> TypedDict('Response', {"status": int, "data": Book}): # type: ignore
    return {"status": 200, "data": await server.post_book(book)}


@app_router.delete("/book/delete/{book_id}", tags=["Книга"])
async def book_delete(book_id: int, server: Annotated[Monolite, Depends(get_monolite_server)]) -> TypedDict('Response', {"status": int, "message": str}): # type: ignore
    await server.book_delete(book_id)
    return {"status": 201, "message": "deleted"}


@app_router.patch("/book/{book_id}", tags=["Книга"])
async def book_update(book_id: int, book: BookUpdate, server: Annotated[Monolite, Depends(get_monolite_server)]) -> Book:
    return await server.book_update(book_id, book)


#Exchange
@app_router.post("/exchange", tags=["Обмен"])
async def exchanges_create(exchange: ExchangeCreate, server: Annotated[Monolite, Depends(get_monolite_server)]) -> TypedDict('Response', {"status": int, "data": Exchange}): # type: ignore
    return {"status": 200, "data": await server.post_exchange(exchange)}


@app_router.get("/exchange", tags=["Обмен"], response_model=ResponseExchangeBook)
async def exchanges_list(exchange_id: int, server: Annotated[Monolite, Depends(get_monolite_server)]) -> Exchange: # type: ignore
    return await server.get_exchange(exchange_id)


@app_router.get("/exchange-list", tags=["Обмен"], response_model=list[ResponseExchangeBook])
async def exchanges_list(server: Annotated[Monolite, Depends(get_monolite_server)]) -> list[Exchange]: # type: ignore
    return await server.get_exchange_list()


@app_router.get("/exchange-sender-list", tags=["Обмен"], response_model=list[ResponseExchangeBook])
async def exchanges_sender_list(sender_id: int, server: Annotated[Monolite, Depends(get_monolite_server)]) -> list[Exchange]: # type: ignore
    return await server.get_exchange_sended_list(sender_id)


@app_router.get("/exchange-receiver-list", tags=["Обмен"], response_model=list[ResponseExchangeBook])
async def exchanges_receiver_list(receiver_id: int, server: Annotated[Monolite, Depends(get_monolite_server)]) -> list[Exchange]: # type: ignore
    return await server.get_exchange_received_list(receiver_id)


@app_router.put("/exchange-books-update", tags=["Обмен"])
async def exchanges_books_update(exchange_id: int, books: BooksChange, server: Annotated[Monolite, Depends(get_monolite_server)]) -> Exchange: # type: ignore
    return await server.get_exchange_received_list(exchange_id, books)


@app_router.delete("/exchange/delete/{exchange_id}", tags=["Обмен"])
async def exchange_delete(exchange_id: int, server: Annotated[Monolite, Depends(get_monolite_server)]) -> TypedDict('Response', {"status": int, "message": str}): # type: ignore
    await server.exchange_delete(exchange_id)
    return {"status": 201, "message": "deleted"}


@app_router.patch("/exchange/accept", tags=["Обмен"])
async def exchange_accept(exchange_id: int, server: Annotated[Monolite, Depends(get_monolite_server)]) -> TypedDict('Response', {"status": int, "message": str}): # type: ignore
    await server.exchange_accept(exchange_id)
    return {"status": 202, "message": "accept"}


@app_router.patch("/exchange/deny", tags=["Обмен"])
async def exchange_deny(exchange_id: int, server: Annotated[Monolite, Depends(get_monolite_server)]) -> TypedDict('Response', {"status": int, "message": str}): # type: ignore
    await server.exchange_deny(exchange_id)
    return {"status": 202, "message": "deny"}