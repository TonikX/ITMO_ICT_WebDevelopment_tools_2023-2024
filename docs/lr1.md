# ЛР №1

В данной лабораторной работе было реализовано серверное приложение с помощью Fast Api.

Был выбран вариант разработки серверной части для программы тайм-менеджмера.

Структура программы:

```plaintext
project/
│
├── auth
│   └── auth.py
│
├── models
│   ├── priority.py
│   ├── project.py
│   ├── tag.py
│   ├── task.py
│   └── user.py
│
├── routers
│   ├── priority.py
│   ├── project.py
│   ├── tag.py
│   ├── task.py
│   └── user.py
│
├── db.py
├── main.py
└── ...
```

Соответственно в папке models лежат модели, в routers - end-point`ы, в db соединения с базой данных, в main основной запуск FastAPI приложения

Рассмотрим каждую часть программы отдельно.

## Main

В файле main.py лежит просто запуск приложения с подключенными роутерами из папки routers.

```python
from fastapi import FastAPI

import db

from routers import *
from models import *

app = FastAPI()
app.include_router(task_router)
app.include_router(tag_router)
app.include_router(priority_router)
app.include_router(project_router)
app.include_router(user_router)


@app.on_event("startup")
def on_startup():
    db.init_db()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, port=3000)

```

## db

В файле db.py лежит соединение с базой данных, а также получение сессию с ней:

```python
from sqlmodel import SQLModel, Session, create_engine
import os
from dotenv import load_dotenv

load_dotenv()

db_url = os.getenv('DB_ADMIN')
engine = create_engine(db_url, echo=True)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session

```

## models

В папке models лежат все файлы, в которых расписаны модели в базе данных. Расмотрим один из основных файлов task.py:

```python
from typing import TYPE_CHECKING, Optional, List
from datetime import date
from sqlmodel import SQLModel, Field, Relationship

from .tag import TagTaskLink
from .priority import Priority
from .tag import Tag

if TYPE_CHECKING:
    from .project import Project


class TaskDefault(SQLModel):
    title: str
    description: str
    dueTo: date
    createdAt: None | date = date.today()
    priority_id: Optional[int] = Field(default=None, foreign_key="priority.id")
    project_id: Optional[int] = Field(default=None, foreign_key="project.id")


class Task(TaskDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    priority: Optional["Priority"] = Relationship(back_populates="tasks_priority")
    tags: Optional[List["Tag"]] | None = Relationship(back_populates="tasks", link_model=TagTaskLink)
    project: Optional["Project"] = Relationship(back_populates="project_tasks")


class TaskOut(TaskDefault):
    id: int
    priority: Optional[Priority] = None
    tags: Optional[List[Tag]] = None
```

## routers

В папке routers лежат все конечные точки, а также описана работа с базой данной, расмотрим также по аналогии с models:

./routers/task.py

```python
from fastapi import APIRouter, Depends
from db import get_session
from typing import List, NotRequired
from typing_extensions import TypedDict
from sqlmodel import select
from models.task import *

router = APIRouter()


@router.get("/task")
def tasks_get(session = Depends(get_session)) -> List[Task]:
    statement = select(Task).order_by(Task.id)
    return session.exec(statement).all()


@router.get("/task/{task_id}")
def task_get(task_id: int, session = Depends(get_session)) -> TypedDict("Response", {"status": int, "data":NotRequired[TaskOut]}):
    task = session.get(Task, task_id)
    if not task:
        return {"status": 404}
    return {"status": 200, "data": task}


@router.post("/task")
def task_post(task: TaskDefault, session = Depends(get_session)):
    task = Task.model_validate(task)
    session.add(task)
    session.commit()
    session.refresh(task)
    return {"status": 201, "data": task}


@router.put("/task/{task_id}")
def task_update(task: TaskDefault, task_id:int, session = Depends(get_session)) -> TypedDict("Response", {"status": int, "data":NotRequired[Task]}):
    task_to_update = session.get(Task, task_id)
    if not task_to_update:
        return {"status": 404}
    task_data = task.model_dump(exclude_unset=True)
    for key, value in task_data.items():
        setattr(task_to_update, key, value)
    session.add(task_to_update)
    session.commit()
    session.refresh(task_to_update)
    return {"status": 201, "data": task_to_update}


@router.delete("/task/{task_id}")
def task_delete(task_id: int, session = Depends(get_session)) -> TypedDict("Response", {"status": int, "data":NotRequired[Task]}):
    task_to_delete = session.get(Task, task_id)
    if not task_to_delete:
        return {"status": 404}
    session.delete(task_to_delete)
    session.commit()
    return {"status": 201, "data": task_to_delete}
```
