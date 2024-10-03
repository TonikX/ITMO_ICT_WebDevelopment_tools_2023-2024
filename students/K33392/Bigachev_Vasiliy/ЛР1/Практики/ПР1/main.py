from fastapi import Body, FastAPI
from pydantic import BaseModel
from typing import Annotated
from models import Task, Tag, Priority
from typing import List, NotRequired
from typing_extensions import TypedDict
import copy

from db import temp_db

app = FastAPI()

@app.get("/tasks")
def tasks_get():
    result_db = copy.deepcopy(temp_db["task"])
    for i, item in enumerate(result_db):
        priority_id = item['priority_id']
        priority = []
        for item in temp_db['priority']:
            if item['id'] == priority_id:
                priority = item
                
        result_db[i].pop('priority_id')
        
        result_db[i]['priority'] = priority

    return result_db

@app.get("/tasks/{task_id}")
def task_get(task_id: int) -> TypedDict('Response', {"status": int, "data": NotRequired[Task]}):
    for item in temp_db['task']:
        if (item['id'] == task_id):
            return {"status": 200, "data": item}
    return {"status": 404}
    

@app.post("/tasks")
def task_post(task: Task) -> TypedDict('Response', {"status": int, "data": NotRequired[Task]}):
    task_to_append = task.model_dump()
    temp_db['task'].append(task_to_append)
    return {"status": 201, "data": task}

@app.put("/tasks/{task_id}")
def task_patch(task_id: int, task: Task) -> TypedDict('Response', {"status": int, "data": NotRequired[Task]}):
    for i, item in enumerate(temp_db["task"]):
        if (item['id'] == task_id):
            temp_db['task'][i] = task
            return {"status": 201, "data": task}
    return {"status": 404}
    
@app.delete("/tasks/{task_id}")
def task_delete(task_id: int) -> TypedDict('Response', {"status": int, "data": NotRequired[Task]}):
    for i, item in enumerate(temp_db["task"]):
        if item.get("id") == task_id:
            temp_db["task"].pop(i)
            return {"status": 201, "data": item}
    return {"status": 404}

@app.get("/priority")
def priority_get() -> list[Priority]:
    return temp_db['priority']

@app.get("/priority/{priority_id}")
def priority(priority_id: int):
    for item in temp_db['priority']:
        if (item['id'] == priority_id):
            return {"status": 200, "data": item}
    return {"status": 404}

@app.post("/priority")
def priority_post(priority: Priority) -> TypedDict('Response', {"status": int, "data": NotRequired[Priority]}):
    priority_to_append = priority.model_dump()
    temp_db['priority'].append(priority_to_append)
    return {"status": 201, "data": priority}

@app.put("/priority/{priority_id}")
def task_patch(priority_id: int, priority: Priority) -> TypedDict('Response', {"status": int, "data": NotRequired[Priority]}):
    for i, item in enumerate(temp_db["priority"]):
        if (item['id'] == priority_id):
            temp_db['priority'][i] = priority
            return {"status": 201, "data": priority}
    return {"status": 404}    
    
@app.delete("/priority/{priority_id}")
def task_delete(priority_id: int) -> TypedDict('Response', {"status": int, "data": NotRequired[Priority]}):
    for i, item in enumerate(temp_db["priority"]):
        if item.get("id") == priority_id:
            temp_db["priority"].pop(i)
            return {"status": 201, "data": item}
    return {"status": 404}