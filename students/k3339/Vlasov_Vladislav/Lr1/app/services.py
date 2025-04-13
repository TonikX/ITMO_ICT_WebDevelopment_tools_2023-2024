from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError

from app.model import (

    BookDefault,
    BookUpdate,
    Book,

    ExchangeCreate,
    ExchangeItem,
    Exchange,
    BooksChange,
    
    ExchangeStatusType,
    DirectionType
)


class Monolite:
    def __init__(self, session: AsyncSession):
        #Данный сервер - монолит. Такая реализация оправдана только сжатыми сроками (сервер был начат создаваться 12.04 15:36)
        self._session = session


    #________Блок с CRUD для Book

    async def post_book(self, dto: BookDefault) -> Book:
        book = Book.model_validate(dto)
        self._session.add(book)
        await self._session.commit()
        await self._session.refresh(book)
        return book


    async def get_book_list(self) -> list[Book]:
        return (await self._session.execute(select(Book))).scalars().all()


    async def get_book(self, book_id) -> Book:
        book = await self._session.get(Book, book_id)
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        return book

    async def book_update(self, book_id: int, dto: BookUpdate) -> Book:
        db_book = await self._session.get(Book, book_id)
        if not db_book:
            raise HTTPException(status_code=404, detail="Book not found")
        
        book_data = dto.model_dump(exclude_unset=True)
        for key, value in book_data.items():
            setattr(db_book, key, value)

        await self._session.commit()
        await self._session.refresh(db_book)
        return db_book


    async def book_delete(self, book_id: int): # type: ignore
        db_book = await self._session.get(Book, book_id)
        if not db_book:
            raise HTTPException(status_code=404, detail="Book not found")
        await self._session.delete(db_book)
        await self._session.commit()


   #________Блок с CRUD для Exchange

    async def post_exchange(self, dto: ExchangeCreate) -> Exchange:
        
        items = dto.items
        dto.items = []
        dto.date = dto.date.replace(tzinfo=None)
        
        exchange = Exchange.model_validate(dto)
        self._session.add(exchange)
        await self._session.commit()
        await self._session.refresh(exchange)

        for item in items:
            exchangeItem = ExchangeItem.model_validate(ExchangeItem(**item.model_dump(), exchange_id = exchange.id))
            self._session.add(exchangeItem)

        await self._session.commit()
        await self._session.refresh(exchange)
        return exchange


    async def get_exchange_list(self) -> list[Exchange]:
        return (await self._session.execute(select(Exchange).options(selectinload(Exchange.items)))).scalars().all()


    async def get_exchange_sended_list(self, sender_id) -> list[Exchange]:
        return (await self._session.execute(select(Exchange).options(selectinload(Exchange.items)).where(Exchange.sender_id == sender_id, Exchange.status == ExchangeStatusType.pending))).scalars().all()
    

    async def get_exchange_received_list(self, receiver_id) -> list[Exchange]:
        return (await self._session.execute(select(Exchange).options(selectinload(Exchange.items)).where(Exchange.receiver_id == receiver_id, Exchange.status == ExchangeStatusType.pending))).scalars().all()


    async def get_exchange(self, exchange_id) -> Exchange:
        exchange = (await self._session.execute(select(Exchange).options(selectinload(Exchange.items)).where(Exchange.id == exchange_id))).scalars().first()
        if not exchange:
            raise HTTPException(status_code=404, detail="Exchange not found")
        return exchange
    

    async def get_exchange_received_list(self, exchange_id, books: BooksChange) -> Exchange:
        db_exchange = await self._session.get(Exchange, exchange_id)
        if not db_exchange:
            raise HTTPException(status_code=404, detail="Exchange not found")
        
        for book in books.new_books:
            self.get_book(book.book_id) #Для проверки существоавния книги
            exchangeItem = ExchangeItem.model_validate(ExchangeItem(**book.model_dump(), exchange_id = db_exchange.id))
            self._session.add(exchangeItem)
       
        for book in books.deleted_books:
            book_id = book.book_id
            exchangeItemDeleted = await self._session.get(ExchangeItem, (exchange_id, book_id))
            if exchangeItemDeleted:
                await self._session.delete(exchangeItemDeleted)

        await self._session.commit()
        await self._session.refresh(db_exchange)
        return db_exchange


    async def exchange_delete(self, exchange_id: int):
        db_exchange = await self._session.get(Exchange, exchange_id)
        if not db_exchange:
            raise HTTPException(status_code=404, detail="Exchange not found")
        await self._session.delete(db_exchange)
        await self._session.commit()


    async def exchange_accept(self, exchange_id: int):
        db_exchange = await self._session.get(Exchange, exchange_id)
        if not db_exchange:
            raise HTTPException(status_code=404, detail="Exchange not found")
        
        if db_exchange.status != ExchangeStatusType.pending:
            raise HTTPException(status_code=400, detail="Exchange not pending")
        
        setattr(db_exchange, "status", ExchangeStatusType.completed)

        await self._session.commit()
        await self._session.refresh(db_exchange)
        exchange = (await self._session.execute(select(Exchange).options(selectinload(Exchange.items)).where(Exchange.id == exchange_id))).scalars().first()
        items = exchange.items

        for item in items:
            exchangeItemDirection = (await self._session.execute(select(ExchangeItem).where(ExchangeItem.exchange_id == exchange_id, ExchangeItem.book_id == item.id))).scalars().first().direction

            if exchangeItemDirection == DirectionType.given:
                new_owner = exchange.receiver_id
            else:
                new_owner = exchange.sender_id

            item.owner_id = new_owner

            for exchange in (await self._session.execute(select(Exchange).options(selectinload(Exchange.items)).where(Exchange.items.any(id=item.id), Exchange.id != exchange_id))).scalars().all():
                exchange.status = ExchangeStatusType.canceled

        await self._session.commit()


    async def exchange_deny(self, exchange_id: int):
        db_exchange = await self._session.get(Exchange, exchange_id)
        if not db_exchange:
            raise HTTPException(status_code=404, detail="Exchange not found")
        
        if db_exchange.status != ExchangeStatusType.pending:
            raise HTTPException(status_code=400, detail="Exchange not pending")
        
        setattr(db_exchange, "status", ExchangeStatusType.canceled)

        await self._session.commit()
        await self._session.refresh(db_exchange)