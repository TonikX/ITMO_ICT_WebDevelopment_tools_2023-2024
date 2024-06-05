# Вспомогательные модули

## Модуль для обращения к БД(синхронный)

```python
from dotenv import dotenv_values
from contextlib import contextmanager
from pathlib import Path
from sqlmodel import Session, create_engine
from typing import Iterator


env_path = Path(__file__).parent.parent / '.env'
config = dotenv_values(env_path)
db_url = config['DB_ADMIN_SYNC']
engine = create_engine(db_url)


@contextmanager
def get_session_context() -> Iterator[Session]:
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()

# Depends зам позаботится о закрытии сессии, когда пишем генератор
def get_session_depends() -> Iterator[Session]:
    with Session(engine) as session:
        yield session
```

## Модуль для связи с БД(асинхронный)
```python

from pathlib import Path

from dotenv import dotenv_values
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from contextlib import asynccontextmanager
from typing import AsyncIterator

env_path = Path(__file__).parent.parent / '.env'
config = dotenv_values(env_path)
db_url = config['DB_ADMIN_ASYNC']

async_engine = create_async_engine(
    db_url,
    future=True
)


async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

@asynccontextmanager
async def get_session_context() -> AsyncIterator[AsyncSession]:
    # для использования в асинхронном контекстном менеджере
    session_maker = async_sessionmaker(
       bind=async_engine, class_=AsyncSession, expire_on_commit=False
    )
    session = session_maker()
    try:
        yield session
    finally:
        await session.close()


async def get_session_depends() -> AsyncIterator[AsyncSession]:
    # Сессия для использования в depends в fastAPI
    async_session = async_sessionmaker(
       bind=async_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
        

async def engine_dispose():
    # Разорвать соединение с БД
    await async_engine.dispose()
```

## Класс для логирования
```python

import logging
import time


# Custom formatter class
class _TimedLogger:
    """Logger class that prefixes each message with elapsed time since instantiation."""

    def __init__(self):
        self.reset_time()

    def reset_time(self):
        self.start_time = time.time()
        self.logger = logging.getLogger("logger")
        self.logger.setLevel(logging.INFO)  # Set the desired default logging level

        # Create a StreamHandler with a custom formatter
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(self._CustomFormatter(self.start_time))

        # Clear existing handlers to avoid duplicate logs in case of reinitialization
        self.logger.handlers = []
        self.logger.addHandler(stream_handler)

    class _CustomFormatter(logging.Formatter):
        """Custom formatter to add time since start to logs."""

        def __init__(self, start_time):
            super().__init__("%(message)s")
            self.start_time = start_time

        def format(self, record):
            elapsed_seconds = time.time() - self.start_time
            # Format time as seconds.milliseconds
            formatted_time = f"{int(elapsed_seconds)}.{int((elapsed_seconds - int(elapsed_seconds)) * 1000)}"
            # Set the prefix with formatted time
            record.msg = f"[{formatted_time}] {record.msg}"
            return super().format(record)

    def info(self, msg):
        self.logger.info(msg)

    def debug(self, msg):
        self.logger.debug(msg)


logger = _TimedLogger()

```


## Класс для работы с категориями

```python
import threading
from sqlalchemy import select
import models

class CategoryManager:
    def __init__(self, project_id, category_none_id):
        self._category_none_id = category_none_id
        self._project_id = project_id
        self._category_locks = {}
        self._category_ids = {}

    def _get_lock(self, category):
        """Retrieve a unique lock for each category."""
        if category not in self._category_locks:
            self._category_locks[category] = threading.Lock()
        return self._category_locks[category]

    def _find_category_obj_db(self, session, category_title):
        query = (
            select(models.Category)
            .where(models.Category.title == category_title)
            .where(models.Category.project_id == self._project_id)
        )
        results = session.exec(query)
        category_obj = results.first()
        if category_obj is None:
            return None
        return category_obj[0].id

    def _create_category_obj(self, session, category_title):
        category_data = {
            "project_id": self._project_id,
            "title": category_title,
            "description": None,
        }
        category_obj = models.Category.model_validate(category_data)
        session.add(category_obj)
        session.commit()
        session.refresh(category_obj)
        return category_obj.id


    def _get_id(self, session, category_title):
        
        category_id = self._category_ids.get(category_title)
        if category_id is not None:
            return category_id
        
        category_id = self._find_category_obj_db(session, category_title)
        if category_id is not None:
            return category_id
        
        category_id = self._create_category_obj(session, category_title)
        return category_id
    
    def get_id(self, session, category_title):
        if category_title is None:
            return self._category_none_id

        with self._get_lock(category_title):
            category_id = self._get_id(session, category_title)
            self._category_ids[category_title] = category_id
            return category_id
```
