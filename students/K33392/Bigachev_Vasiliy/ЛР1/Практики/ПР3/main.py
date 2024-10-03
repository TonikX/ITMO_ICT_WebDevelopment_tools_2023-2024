from fastapi import Body, FastAPI, Depends
from pydantic import BaseModel
from typing import Annotated
from typing import List, NotRequired
from typing_extensions import TypedDict
import copy
from sqlalchemy.orm import joinedload 
from db import init_db, get_session
from models import Task, Priority, PriorityDefault, TaskDefault, TaskOut, TagDefault, Tag
from sqlmodel import select

from datetime import date, datetime

app = FastAPI()

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/task")
def tasks_get(session = Depends(get_session)) -> List[TaskOut]:
    # Отображение вложенного объекта нормального не нашлось, ничего не работало
    statement = select(Task)
    return session.exec(statement).all()

@app.get("/task/{task_id}")
def task_get(task_id: int, session = Depends(get_session)) -> TypedDict("Response", {"status": int, "data":NotRequired[TaskOut]}):
    task = session.get(Task, task_id)
    if not task:
        return {"status": 404}
    return {"status": 200, "data": task}

@app.post("/task")
def task_post(task: TaskDefault, session = Depends(get_session)):
    task = Task.model_validate(task)
    session.add(task)
    session.commit()
    session.refresh(task)
    return {"status": 201, "data": task}

@app.put("/task/{task_id}")
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

@app.delete("/task/{task_id}")
def task_delete(task_id: int, session = Depends(get_session)) -> TypedDict("Response", {"status": int, "data":NotRequired[Task]}):
    task_to_delete = session.get(Task, task_id)
    if not task_to_delete:
        return {"status": 404}
    session.delete(task_to_delete)
    session.commit()
    return {"status": 201, "data": task_to_delete}

@app.get("/priority")
def priority_get(session = Depends(get_session)) -> TypedDict("Response", {"status": int, "data":NotRequired[List[Priority]]}):
    statement = select(Priority)
    result = session.exec(statement).all()
    if not result:
        return {"status": 404}
    return {"status": 200, "data": result}

@app.post("/priority")
def priority_post(priority: PriorityDefault, session = Depends(get_session)) -> TypedDict("Response", {"status": int, "data":NotRequired[Priority]}):
    priority = Priority.model_validate(priority)
    session.add(priority)
    session.commit()
    session.refresh(priority)
    return {"status": 201, "data": priority}

@app.get("/priority/{priority_id}")
def priority_get_by_id(priority_id: int, session = Depends(get_session)) -> TypedDict("Response", {"status": int, "data":NotRequired[Priority]}):
    priority = session.get(Priority, priority_id)
    if not priority:
        return {"status": 404}
    return {"status": 200, "data": priority}

@app.put("/priority/{priority_id}")
def priority_update(priority_id: int, priority: PriorityDefault, session = Depends(get_session)) -> TypedDict("Response", {"status": int, "data":NotRequired[Priority]}):
    priority_to_update = session.get(Priority, priority_id)
    if not priority_to_update:
        return {"status": 404}
    priority_data = priority.model_dump(exclude_unset=True)
    for key, value in priority_data.items():
        setattr(priority_to_update, key, value)
    session.add(priority_to_update)
    session.commit()
    session.refresh(priority_to_update)
    return {"status": 201, "data": priority_to_update}

@app.delete("/priority/{priority_id}")
def priority_update(priority_id: int, session = Depends(get_session)) -> TypedDict("Response", {"status": int, "data":NotRequired[Priority]}):
    priority_to_delete = session.get(Priority, priority_id)
    if not priority_to_delete:
        return {"status": 404}
    session.delete(priority_to_delete)
    session.commit()
    return {"status": 201, "data": priority_to_delete}

@app.post("/tag")
def tag_post(tag: TagDefault, session = Depends(get_session)) -> TypedDict("Response", {"status": int, "data":NotRequired[Tag]}):
    tag = Tag.model_validate(tag)
    session.add(tag)
    session.commit()
    session.refresh(tag)
    return {"status": 201, "data": tag}

@app.get("/tag")
def tag_get(session = Depends(get_session)) -> TypedDict("Response", {"status": int, "data":NotRequired[List[Tag]]}):
    statement = select(Tag)
    result = session.exec(statement).all()
    if not result:
        return {"status": 404}
    return {"status": 200, "data": result}
    
@app.delete("/tag/{tag_id}")
def priority_update(tag_id: int, session = Depends(get_session)) -> TypedDict("Response", {"status": int, "data":NotRequired[Tag]}):
    tag_to_delete = session.get(Tag, tag_id)
    if not tag_to_delete:
        return {"status": 404}
    session.delete(tag_to_delete)
    session.commit()
    return {"status": 201, "data": tag_to_delete}


# Добавление тэга к задаче
@app.patch("/addTagToTask")
def add_tag_to_task(task_id: int, tag_id: int, session = Depends(get_session)) -> TypedDict("Response", {"status": int}):
    task = session.get(Task, task_id)
    tag = session.get(Tag, tag_id)
    
    tag.tasks.append(task)
    session.add(tag)
    session.commit()
    return {"status": 201}

# Удаление тэга из задачи
@app.patch("/delTagFromTask")
def del_tag_from_task(task_id: int, tag_id: int, session = Depends(get_session)) -> TypedDict("Response", {"status": int}):
    task = session.get(Task, task_id)
    tag = session.get(Tag, tag_id)
    
    task.tags.remove(tag)
    session.add(task)
    session.commit()
    return {"status": 201}