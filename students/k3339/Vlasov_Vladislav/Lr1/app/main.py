from typing import Annotated
from sqlmodel import select
from typing_extensions import TypedDict
from fastapi import APIRouter, Depends, FastAPI, HTTPException

from services import Monolite
from depends import get_monolite_server
from connection import get_session, init_db

from model import (
    ProfileDefault,
    ProfileUpdate,
    Profile,

    BookDefault,
    BookUpdate,
    Book,

    AccountDefault,
    AccountUpdate,
    Account,

    ExchangeDefault,
    ExchangeCreate,
    Exchange,
    BooksChange,

    ExchangeItem,

    ResponseAccountProfile,
    ResponseExchangeBook,
)

app = FastAPI()

router = APIRouter()


@app.on_event("startup")
async def on_startup():
    await init_db()

#Account

@router.get("/accounts_list", tags=["Аккаунт"])
async def accounts_list(server: Annotated[Monolite, Depends(get_monolite_server)]) -> list[Account]:
    return await server.get_user_list()


@router.get("/account/{account_id}", tags=["Аккаунт"] , response_model=ResponseAccountProfile)
async def get_accounts(account_id: int, server: Annotated[Monolite, Depends(get_monolite_server)]) -> Account:
    return await server.get_user(account_id)


@router.post("/account", tags=["Аккаунт"])
async def accounts_create(account: AccountDefault, server: Annotated[Monolite, Depends(get_monolite_server)]) -> TypedDict('Response', {"status": int, "data": Account}): # type: ignore
    return {"status": 200, "data": await server.post_user(account)}



@router.delete("/account/delete/{account_id}", tags=["Аккаунт"])
async def account_delete(account_id: int, server: Annotated[Monolite, Depends(get_monolite_server)]) -> TypedDict('Response', {"status": int, "message": str}): # type: ignore
    await server.user_delete(account_id)
    return {"status": 201, "message": "deleted"}


@router.patch("/account/{account_id}", tags=["Аккаунт"])
async def account_update(account_id: int, account: AccountUpdate, server: Annotated[Monolite, Depends(get_monolite_server)]) -> Account:
    return await server.user_update(account_id, account)


#Profile

@router.get("/profiles_list", tags=["Профиль"])
async def profiles_list(server: Annotated[Monolite, Depends(get_monolite_server)]) -> list[Profile]:
    return await server.get_profile_list()


@router.get("/profiles_for_account", tags=["Профиль"])
async def profile_for_account(account_id: int, server: Annotated[Monolite, Depends(get_monolite_server)]) -> Profile:
    return await server.get_profile_for_account(account_id)


@router.get("/profile/{profile_id}", tags=["Профиль"])
async def get_profiles(profile_id: int, server: Annotated[Monolite, Depends(get_monolite_server)]) -> Profile:
    return await server.get_profile(profile_id)



@router.patch("/profile/{profile_id}", tags=["Профиль"])
async def profile_update(profile_id: int, profile: ProfileUpdate, server: Annotated[Monolite, Depends(get_monolite_server)]) -> Profile:
    return await server.profile_update(profile_id, profile)


#Book


@router.get("/books_list", tags=["Книга"])
async def books_list(server: Annotated[Monolite, Depends(get_monolite_server)]) -> list[Book]:
    return await server.get_book_list()


@router.get("/book/{book_id}", tags=["Книга"])
async def get_books(book_id: int, server: Annotated[Monolite, Depends(get_monolite_server)]) -> Book:
    return await server.get_book(book_id)


@router.post("/book", tags=["Книга"])
async def books_create(book: BookDefault, server: Annotated[Monolite, Depends(get_monolite_server)]) -> TypedDict('Response', {"status": int, "data": Book}): # type: ignore
    return {"status": 200, "data": await server.post_book(book)}


@router.delete("/book/delete/{book_id}", tags=["Книга"])
async def book_delete(book_id: int, server: Annotated[Monolite, Depends(get_monolite_server)]) -> TypedDict('Response', {"status": int, "message": str}): # type: ignore
    await server.book_delete(book_id)
    return {"status": 201, "message": "deleted"}


@router.patch("/book/{book_id}", tags=["Книга"])
async def book_update(book_id: int, book: BookUpdate, server: Annotated[Monolite, Depends(get_monolite_server)]) -> Book:
    return await server.book_update(book_id, book)


#Exchange
@router.post("/exchange", tags=["Обмен"])
async def exchanges_create(exchange: ExchangeCreate, server: Annotated[Monolite, Depends(get_monolite_server)]) -> TypedDict('Response', {"status": int, "data": Exchange}): # type: ignore
    return {"status": 200, "data": await server.post_exchange(exchange)}


@router.get("/exchange", tags=["Обмен"], response_model=ResponseExchangeBook)
async def exchanges_list(exchange_id: int, server: Annotated[Monolite, Depends(get_monolite_server)]) -> Exchange: # type: ignore
    return await server.get_exchange(exchange_id)


@router.get("/exchange-list", tags=["Обмен"], response_model=list[ResponseExchangeBook])
async def exchanges_list(server: Annotated[Monolite, Depends(get_monolite_server)]) -> list[Exchange]: # type: ignore
    return await server.get_exchange_list()


@router.get("/exchange-sender-list", tags=["Обмен"], response_model=list[ResponseExchangeBook])
async def exchanges_sender_list(sender_id: int, server: Annotated[Monolite, Depends(get_monolite_server)]) -> list[Exchange]: # type: ignore
    return await server.get_exchange_sended_list(sender_id)


@router.get("/exchange-receiver-list", tags=["Обмен"], response_model=list[ResponseExchangeBook])
async def exchanges_receiver_list(receiver_id: int, server: Annotated[Monolite, Depends(get_monolite_server)]) -> list[Exchange]: # type: ignore
    return await server.get_exchange_received_list(receiver_id)


@router.put("/exchange-books-update", tags=["Обмен"])
async def exchanges_books_update(exchange_id: int, books: BooksChange, server: Annotated[Monolite, Depends(get_monolite_server)]) -> Exchange: # type: ignore
    return await server.get_exchange_received_list(exchange_id, books)


@router.delete("/exchange/delete/{exchange_id}", tags=["Обмен"])
async def exchange_delete(exchange_id: int, server: Annotated[Monolite, Depends(get_monolite_server)]) -> TypedDict('Response', {"status": int, "message": str}): # type: ignore
    await server.exchange_delete(exchange_id)
    return {"status": 201, "message": "deleted"}


@router.patch("/exchange/accept", tags=["Обмен"])
async def exchange_accept(exchange_id: int, server: Annotated[Monolite, Depends(get_monolite_server)]) -> TypedDict('Response', {"status": int, "message": str}): # type: ignore
    await server.exchange_accept(exchange_id)
    return {"status": 202, "message": "accept"}


@router.patch("/exchange/deny", tags=["Обмен"])
async def exchange_deny(exchange_id: int, server: Annotated[Monolite, Depends(get_monolite_server)]) -> TypedDict('Response', {"status": int, "message": str}): # type: ignore
    await server.exchange_deny(exchange_id)
    return {"status": 202, "message": "deny"}


app.include_router(router)