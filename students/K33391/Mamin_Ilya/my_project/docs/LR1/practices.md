# Практические работы

## Описание

В рамках работы были также реализованы и практические работы на основе задания лабораторной работы про программу-тайм-менеджера.

## ПР1 
Было необходимо: 

1. Сделать временную базу для главной таблицы (2-3 записи), по аналогии с практикой (должны иметь одиночный вложенный объект и список объектов)
2. Выполнить действия описанные в практике для своего проекта
3. Сделать модели и API для вложенного объекта


### db.py
```python 
temp_db = [
    {
        "task_id": 1,
        "task": "Complete project",
        "description": "Finish the task manager app",
        "deadline": "2022-12-31",
        "priority": "High",
        "time_spent": 120,
    },
    {
        "task_id": 2,
        "task": "Write documentation",
        "description": "Document the task manager app",
        "deadline": "2022-12-31",
        "priority": "Medium",
        "time_spent": 50,
    },
    {
        "task_id": 3,
        "task": "Test application",
        "description": "Test the task manager app",
        "deadline": "2022-12-31",
        "priority": "Low",
        "time_spent": 0,
    },
]

```

###main.py 

```python
from fastapi import FastAPI
from models import *
from typing_extensions import TypedDict
from db import temp_db
from typing import Optional, List
import uvicorn

app = FastAPI()


@app.get("/")
def hello():
    return "Hello, user!"


@app.post("/create_task")
def create_task(task: Task):
    temp_db.append(task)

    return {"status": 200, "data": task}


@app.put("/update_task/{task_id}")
def update_task(task_id: int, task: TaskDefault):
    for task in temp_db:
        if task["task_id"] == task_id:
            task["title"] = task["title"]
            task["description"] = task["description"]
            task["deadline"] = task["deadline"]
            task["priority"] = task["priority"]
            task["time_spent"] = task["time_spent"]
            return {"status": 200, "data": task}
    else:
        return {"status": 404, "data": "Task not found"}


@app.delete("/delete_task/{task_id}")
def delete_task(task_id: int):
    for task in temp_db:
        if task["task_id"] == task_id:
            temp_db.remove(task)
            return {"status": 200, "data": "Task deleted"}
    else:
        return {"status": 404, "data": "Task not found"}


@app.get("/tasks")
def get_tasks():
    return temp_db


@app.get("/task/{task_id}")
def get_task(task_id: int):
    for task in temp_db:
        if task["task_id"] == task_id:
            return task
    return {"status": 404, "data": "Task not found"}


@app.get("/tasks/{task_id}/time")
def get_task_time(task_id: int):
    for task in temp_db:
        if task["task_id"] == task_id:
            return task["time_spent"]
    return {"status": 404, "data": "Task not found"}


@app.put("/tasks/{task_id}/time")
def track_time_spent(task_id: int, time_spent: int):
    for task in temp_db:
        if task["task_id"] == task_id:
            task["time_spent"] = time_spent
            return {"status": 200, "data": task}
    return {"status": 404, "data": task}
```
### models.py

```python
import datetime
from pydantic import BaseModel
from enum import Enum
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship


class Priority(Enum):
    high = "high"
    medium = "medium"
    low = "low"
    no_priority = "no_priority"


class TaskDefault(SQLModel):
    title: str
    description: Optional[str] = None
    deadline: datetime.date
    priority: Priority = Priority.no_priority


class TaskShow(TaskDefault):
    title: str
    deadline: datetime.date
    priority: Priority
    time_spent: Optional[int] = None


class Task(TaskDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    time_spent: Optional[int] = None
```

## ПР2

Было необходимо:

1. Пошагово реализовать подключение к БД, АПИ и модели, на основании своего варианта основываясь на действиях в практике
2. Сделать модели и API для many-to-many связей с вложенным отображением.

### db.py

```python
from sqlmodel import SQLModel, Session, create_engine

db_url = 'postgresql://postgres:123@localhost:5432/pr2'
engine = create_engine(db_url, echo=True)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
```
### endpoints.py

```python
import datetime
from fastapi import APIRouter, HTTPException, Depends
from models import *
from db import get_session
from typing_extensions import TypedDict
from sqlmodel import SQLModel, create_engine
from sqlmodel.sql.expression import select

app_router = APIRouter()

@app_router.post("/create_task", tags=["tasks"])
def create_task(task: Task, session=Depends(get_session)):
    session.add(task)
    session.commit()
    session.refresh(task)

    return {"status": 200, "data": task}


@app_router.put("/update_task/{task_id}", tags=["tasks"])
def update_task(task_id: int, task: TaskUpdate, session=Depends(get_session)):
    db_task = session.get(Task, task_id)
    if not db_task:
        return ({'status': 404, 'data': 'Task not found'})

    task_data = task.model_dump(exclude_unset=True)
    for key, value in task_data.items():
        setattr(db_task, key, value)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


@app_router.delete("/delete_task/{task_id}", tags=["tasks"])
def delete_task(task_id: int, session=Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        return ({'status': 404, 'data': 'Task not found'})
    session.delete(task)
    session.commit()
    return {"ok": True}


@app_router.get("/tasks", tags=["tasks"],)
def get_tasks(session=Depends(get_session)):
    return session.exec(select(Task)).all()


@app_router.get("/task/{task_id}", tags=["tasks"])
def get_task(task_id: int, session=Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        return ({'status': 404, 'data': 'Task not found'})
    return task


@app_router.get("/tasks/{task_id}/time", tags=["tasks"])
def get_task_time(task_id: int, session=Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        return ({'status': 404, 'data': 'Task not found'})
    return {"time_spent": task.time_spent}


@app_router.put("/tasks/{task_id}/time", tags=["tasks"])
def track_time_spent(task_id: int, time_spent: int, session=Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        return ({'status': 404, 'data': 'Task not found'})
    task.time_spent = time_spent
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

```
### main.py

```python
from fastapi import FastAPI
import uvicorn
from db import init_db
from endpoints import app_router

app = FastAPI()

app.include_router(app_router, prefix="/api", tags=["main"])


@app.on_event("startup")
def on_startup():
    init_db()


if __name__ == '__main__':
    uvicorn.run('main:app', host="localhost", port=8000, reload=True)
```

### models.py

```python
import datetime
from pydantic import BaseModel
from enum import Enum
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship


class Priority(Enum):
    high = "high"
    medium = "medium"
    low = "low"
    no_priority = "no_priority"


class TaskDefault(SQLModel):
    title: str
    description: Optional[str] = None
    deadline: datetime.date
    priority: Priority = Priority.no_priority


class TaskShow(TaskDefault):
    title: str
    deadline: datetime.date
    priority: Priority
    time_spent: Optional[int] = None


class Task(TaskDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    time_spent: Optional[int] = None
    schedules: Optional[List["Schedule"]] = Relationship(back_populates="task")
    reminders: Optional[List["Reminder"]] = Relationship(back_populates="task")


class ScheduleDefault(SQLModel):
    task_id: Optional[int] = Field(default=None, foreign_key="task.id")
    date: datetime.date
    start_time: datetime.time
    end_time: datetime.time


class ScheduleShow(ScheduleDefault):
    task: Optional["Task"] = None


class Schedule(ScheduleDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    task: Optional["Task"] = Relationship(back_populates="schedules")


class ReminderDefault(SQLModel):
    task_id: Optional[int] = Field(default=None, foreign_key="task.id")
    remind_at: datetime.datetime


class ReminderShow(ReminderDefault):
    task: Optional[Task] = None


class Reminder(ReminderDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    task_id: Optional[int] = Field(default=None, foreign_key="task.id")
    task: Optional["Task"] = Relationship(back_populates="reminders")

```

## ПР3

Было необходимо:

1. Реализовать в своем проекте все улучшения, описанные в практике
2. Разобраться как передать в alembic.ini URL базы данных с помощью.env-файла и реализовать подобную передачу.

### db.py

```python
from sqlmodel import SQLModel, Session, create_engine

db_url = 'postgresql://postgres:123@localhost:5432/pr3'
engine = create_engine(db_url, echo=True)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
```

### endpoints.py

```python
import datetime
from fastapi import APIRouter, HTTPException, Depends
from models import (
    TaskDefault, Task, TaskShow,
    ScheduleDefault, ScheduleShow, Schedule,
    ReminderDefault, ReminderShow, Reminder,
)
from db import get_session
from typing_extensions import TypedDict

logic_router = APIRouter()

@logic_router.post("/task-create")
def task_create(task: TaskDefault, session=Depends(get_session)) -> TypedDict('Response', {"status": int, "data": Task}):
    task = Task.model_validate(task)
    session.add(task)
    session.commit()
    session.refresh(task)
    return {"status": 200, "data": task}

@logic_router.get("/list-tasks")
def tasks_list(session=Depends(get_session)) -> list[Task]:
    return session.query(Task).all()

@logic_router.get("/task/{task_id}", response_model=TaskShow)
def task_get(task_id: int, session=Depends(get_session)):
    obj = session.get(Task, task_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="task not found")
    return obj

@logic_router.patch("/task/update/{task_id}")
def task_update(task_id: int, task: TaskDefault, session=Depends(get_session)) -> Task:
    db_task = session.get(Task, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="task not found")

    task_data = task.model_dump(exclude_unset=True)
    for key, value in task_data.items():
        setattr(db_task, key, value)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

@logic_router.delete("/task/delete/{task_id}")
def task_delete(task_id: int, session=Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="task not found")
    session.delete(task)
    session.commit()
    return {"ok": True}

@logic_router.post("/schedule-create")
def schedule_create(schedule: ScheduleDefault, session=Depends(get_session)) -> TypedDict('Response', {"status": int, "data": Schedule}):
    schedule = Schedule.model_validate(schedule)
    session.add(schedule)
    session.commit()
    session.refresh(schedule)
    return {"status": 200, "data": schedule}

@logic_router.get("/list-schedules")
def schedules_list(session=Depends(get_session)) -> list[Schedule]:
    return session.query(Schedule).all()

@logic_router.get("/schedule/{schedule_id}", response_model=ScheduleShow)
def schedule_get(schedule_id: int, session=Depends(get_session)):
    obj = session.get(Schedule, schedule_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="schedule not found")
    return obj

@logic_router.patch("/schedule/update/{schedule_id}")
def schedule_update(schedule_id: int, schedule: ScheduleDefault, session=Depends(get_session)) -> Schedule:
    db_schedule = session.get(Schedule, schedule_id)
    if not db_schedule:
        raise HTTPException(status_code=404, detail="schedule not found")

    schedule_data = schedule.model_dump(exclude_unset=True)
    for key, value in schedule_data.items():
        setattr(db_schedule, key, value)
    session.add(db_schedule)
    session.commit()
    session.refresh(db_schedule)
    return db_schedule

@logic_router.delete("/schedule/delete/{schedule_id}")
def schedule_delete(schedule_id: int, session=Depends(get_session)):
    schedule = session.get(Schedule, schedule_id)
    if not schedule:
        raise HTTPException(status_code=404, detail="schedule not found")
    session.delete(schedule)
    session.commit()
    return {"ok": True}

@logic_router.post("/reminder-create")
def reminder_create(reminder: ReminderDefault, session=Depends(get_session)) -> TypedDict('Response', {"status": int, "data": Reminder}):
    reminder = Reminder.model_validate(reminder)
    session.add(reminder)
    session.commit()
    session.refresh(reminder)
    return {"status": 200, "data": reminder}

@logic_router.get("/list-reminders")
def reminders_list(session=Depends(get_session)) -> list[Reminder]:
    return session.query(Reminder).all()

@logic_router.get("/reminder/{reminder_id}", response_model=ReminderShow)
def reminder_get(reminder_id: int, session=Depends(get_session)):
    obj = session.get(Reminder, reminder_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="reminder not found")
    return obj

@logic_router.patch("/reminder/update/{reminder_id}")
def reminder_update(reminder_id: int, reminder: ReminderDefault, session=Depends(get_session)) -> Reminder:
    db_reminder = session.get(Reminder, reminder_id)
    if not db_reminder:
        raise HTTPException(status_code=404, detail="reminder not found")

    reminder_data = reminder.model_dump(exclude_unset=True)
    for key, value in reminder_data.items():
        setattr(db_reminder, key, value)
    session.add(db_reminder)
    session.commit()
    session.refresh(db_reminder)
    return db_reminder

@logic_router.delete("/reminder/delete/{reminder_id}")
def reminder_delete(reminder_id: int, session=Depends(get_session)):
    reminder = session.get(Reminder, reminder_id)
    if not reminder:
        raise HTTPException(status_code=404, detail="reminder not found")
    session.delete(reminder)
    session.commit()
    return {"ok": True}

@logic_router.patch("/task/{task_id}/add-time")
def add_time_to_task(task_id: int, time_spent: int, session=Depends(get_session)) -> Task:
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="task not found")
    if task.time_spent is None:
        task.time_spent = 0
    task.time_spent += time_spent
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@logic_router.post("/reminder/{reminder_id}/copy-for-task/{task_id}")
def copy_reminder_for_task(reminder_id: int, task_id: int, session=Depends(get_session)):
    reminder = session.get(Reminder, reminder_id)
    if not reminder:
        raise HTTPException(status_code=404, detail="reminder not found")
    
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="task not found")
    
    new_reminder = Reminder(
        task_id=task_id,
        remind_at=reminder.remind_at
    )
    session.add(new_reminder)
    session.commit()
    session.refresh(new_reminder)
    return {"status": 200, "message": "Reminder copied for new task successfully"}
```

### main.py

```python
from fastapi import FastAPI
import uvicorn
from db import init_db
from endpoints import logic_router


app = FastAPI()

app.include_router(logic_router, prefix="/api", tags=["main"])


@app.on_event("startup")
def on_startup():
    init_db()


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)

```

### models.py

```python
import datetime
from pydantic import BaseModel
from enum import Enum
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship


class Priority(Enum):
    high = "high"
    medium = "medium"
    low = "low"
    no_priority = "no_priority"


class TaskDefault(SQLModel):
    title: str
    description: Optional[str] = None
    deadline: datetime.date
    priority: Priority = Priority.no_priority


class TaskShow(TaskDefault):
    title: str
    deadline: datetime.date
    priority: Priority
    time_spent: Optional[int] = None


class Task(TaskDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    time_spent: Optional[int] = None
    schedules: Optional[List["Schedule"]] = Relationship(back_populates="task")
    reminders: Optional[List["Reminder"]] = Relationship(back_populates="task")


class ScheduleDefault(SQLModel):
    task_id: Optional[int] = Field(default=None, foreign_key="task.id")
    date: datetime.date
    start_time: datetime.time
    end_time: datetime.time


class ScheduleShow(ScheduleDefault):
    task: Optional["Task"] = None


class Schedule(ScheduleDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    task: Optional["Task"] = Relationship(back_populates="schedules")


class ReminderDefault(SQLModel):
    task_id: Optional[int] = Field(default=None, foreign_key="task.id")
    remind_at: datetime.datetime


class ReminderShow(ReminderDefault):
    task: Optional[Task] = None


class Reminder(ReminderDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    task_id: Optional[int] = Field(default=None, foreign_key="task.id")
    task: Optional["Task"] = Relationship(back_populates="reminders")

```