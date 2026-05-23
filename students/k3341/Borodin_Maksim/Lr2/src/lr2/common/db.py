from functools import lru_cache

from sqlmodel import Session, SQLModel, create_engine

from lr2.common.config import get_settings


@lru_cache
def get_engine():
    settings = get_settings()
    return create_engine(settings.database_url, echo=False)


def get_session() -> Session:
    return Session(get_engine())


def ensure_parsed_pages_table() -> None:
    from lr2.common.models import ParsedPage

    SQLModel.metadata.create_all(get_engine(), tables=[ParsedPage.__table__])
