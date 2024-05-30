import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Author, Book

SQLALCHEMY_DATABASE_URL = "postgresql://book_crossing:book_crossing@localhost:5432/book_crossing"
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def save_to_db(data: str):
    data_dict = json.loads(data)

    print(data)

    session = SessionLocal()

    try:
        author_name = data_dict.get('author_name')

        if not author_name:
            raise ValueError("Некорректные данные")

        author = Author(name=author_name)

        book_names = data_dict.get('books')

        if not book_names:
            raise ValueError("Некорректные данные")

        books = [Book(name=title, author=author) for title in book_names]

        session.add(author)
        session.add_all(books)

        session.commit()
        session.refresh(author)

        return author, books

    finally:
        session.close()