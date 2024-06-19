import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model.models import Author, Book
import os
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv("DB_ADMIN")

# Подключение к базе данных
engine = create_engine(db_url, echo=True)

# Создание сессии
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def save_author_and_books_from_json(data: str):
    # Декодирование JSON-данных
    data_dict = json.loads(data)

    # Создание сессии
    session = SessionLocal()

    try:
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
        session.commit()
        session.refresh(author)

        return author, books

    finally:
        # Закрытие сессии
        session.close()
