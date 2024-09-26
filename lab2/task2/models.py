import datetime

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from db import engine
from enums import ParseMethod


class Base(DeclarativeBase):
    pass


class Title(Base):
    __tablename__ = "titles"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    parse_method: Mapped[ParseMethod]
    url: Mapped[str]
    title: Mapped[str]
    created_at: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now)


def create_db_and_tables() -> None:
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    create_db_and_tables()