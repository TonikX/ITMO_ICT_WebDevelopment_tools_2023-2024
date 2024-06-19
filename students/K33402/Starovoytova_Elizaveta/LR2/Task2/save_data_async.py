import json
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.future import select
from models import Author, Book

# Подключение к базе данных
SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://postgres:123@localhost/bookcross_db"
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)


async def save_author_and_books_from_json(data: str):
    # Декодирование JSON-данных
    data_dict = json.loads(data)

    # Создание асинхронной сессии
    async with AsyncSession(engine) as session:
        # Извлечение данных об авторе из JSON
        author_name = data_dict.get('author_name')

        if not author_name:
            raise ValueError("Недостаточно данных для сохранения.")

        # Создание объекта Author
        author = Author(name=author_name, bio="")

        # Извлечение списка книг из JSON
        book_titles = data_dict.get('books')

        if not book_titles:
            raise ValueError("Не указан список книг для сохранения.")

        # Создание объектов Book и их добавление к автору
        books = [Book(title=title, description="", author=author) for title in book_titles]

        # Добавление объектов в сессию
        session.add(author)
        session.add_all(books)

        # Сохранение изменений
        await session.commit()

        # Запрос на получение сохраненного автора
        await session.refresh(author)

        return author, books
