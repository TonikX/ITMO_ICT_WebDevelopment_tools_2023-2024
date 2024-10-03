from fastapi import APIRouter, Depends
from db import get_session
from typing import List, NotRequired
from typing_extensions import TypedDict
from sqlmodel import select
from models.tag import *
from models.task import Task

router = APIRouter()

@router.post("/tag")
def tag_post(tag: TagDefault, session = Depends(get_session)) -> TypedDict("Response", {"status": int, "data":NotRequired[Tag]}):
    tag = Tag.model_validate(tag)
    session.add(tag)
    session.commit()
    session.refresh(tag)
    return {"status": 201, "data": tag}

@router.get("/tag")
def tag_get(session = Depends(get_session)) -> TypedDict("Response", {"status": int, "data":NotRequired[List[Tag]]}):
    statement = select(Tag)
    result = session.exec(statement).all()
    if not result:
        return {"status": 404}
    return {"status": 200, "data": result}
    
@router.delete("/tag/{tag_id}")
def priority_update(tag_id: int, session = Depends(get_session)) -> TypedDict("Response", {"status": int, "data":NotRequired[Tag]}):
    tag_to_delete = session.get(Tag, tag_id)
    if not tag_to_delete:
        return {"status": 404}
    session.delete(tag_to_delete)
    session.commit()
    return {"status": 201, "data": tag_to_delete}


# Добавление тэга к задаче
@router.patch("/addTagToTask")
def add_tag_to_task(task_id: int, tag_id: int, session = Depends(get_session)) -> TypedDict("Response", {"status": int}):
    task = session.get(Task, task_id)
    tag = session.get(Tag, tag_id)
    
    tag.tasks.append(task)
    session.add(tag)
    session.commit()
    return {"status": 201}

# Удаление тэга из задачи
@router.patch("/delTagFromTask")
def del_tag_from_task(task_id: int, tag_id: int, session = Depends(get_session)) -> TypedDict("Response", {"status": int}):
    task = session.get(Task, task_id)
    tag = session.get(Tag, tag_id)
    
    task.tags.remove(tag)
    session.add(task)
    session.commit()
    return {"status": 201}