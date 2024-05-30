import json
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from models import Author, Book

SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://book_crossing:book_crossing@localhost:5432/book_crossing"
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)


async def save_to_db(data: str):
    data_dict = json.loads(data)

    async with AsyncSession(engine) as session:
        author_name = data_dict.get('author_name')

        if not author_name:
            raise ValueError("Некорректные данные")

        author = Author(name=author_name)

        book_titles = data_dict.get('books')

        if not book_titles:
            raise ValueError("Некорректные данные")

        books = [Book(name=title, author=author) for title in book_titles]

        session.add(author)
        session.add_all(books)

        await session.commit()
        await session.refresh(author)

        return author, books
