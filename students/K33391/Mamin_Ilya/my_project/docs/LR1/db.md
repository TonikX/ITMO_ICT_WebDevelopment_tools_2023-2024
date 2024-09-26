# Модуль базы данных

Этот модуль предоставляет функционал для работы с базой данных и инициализации ее структуры.

## Описание

Модуль включает в себя функции для создания таблиц базы данных и управления данными.

## Код

```python
from sqlmodel import SQLModel, Session, create_engine
import os
from dotenv import load_dotenv

load_dotenv()
engine = create_engine(os.getenv("DB_URL"), echo=True)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
```