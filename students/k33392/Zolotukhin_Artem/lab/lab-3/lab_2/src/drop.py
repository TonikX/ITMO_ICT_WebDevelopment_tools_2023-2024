from sqlmodel import Session, select, delete
from .db import engine, Book


def start():
    with Session(engine) as session:
        statement = delete(Book)
        session.exec(statement)  # type: ignore
        session.commit()


if __name__ == "__main__":
    start()
