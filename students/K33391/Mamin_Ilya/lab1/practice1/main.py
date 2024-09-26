from fastapi import FastAPI
from models import Task, TaskDefault, TaskCreate
from typing_extensions import TypedDict
from db import temp_db
from typing import Optional, List
import uvicorn

app = FastAPI()

current_task_id = 4

@app.get("/")
def hello():
    return "Hello, user!"

@app.post("/create_task")
def create_task(task: TaskCreate):
    global current_task_id
    task_data = task.dict()  
    task_data["task_id"] = current_task_id  
    temp_db.append(task_data)  
    current_task_id += 1  
    return {"status": 200, "data": task_data}

@app.put("/update_task/{task_id}")
def update_task(task_id: int, task_data: TaskDefault):
    for task in temp_db:
        if task["task_id"] == task_id:
            task["title"] = task_data.title
            task["description"] = task_data.description
            task["deadline"] = task_data.deadline
            task["priority"] = task_data.priority
            task["time_spent"] = task_data.time_spent
            return {"status": 200, "data": task}
    return {"status": 404, "data": "Task not found"}

@app.delete("/delete_task/{task_id}")
def delete_task(task_id: int):
    for task in temp_db:
        if task["task_id"] == task_id:
            temp_db.remove(task)
            return {"status": 200, "data": "Task deleted"}
    return {"status": 404, "data": "Task not found"}

@app.get("/tasks")
def get_tasks():
    return temp_db

@app.get("/task/{task_id}")
def get_task(task_id: int):
    for task in temp_db:
        if task["task_id"] == task_id:
            return {"status": 200, "data": task}
    return {"status": 404, "data": "Task not found"}

@app.get("/tasks/{task_id}/time")
def get_task_time(task_id: int):
    for task in temp_db:
        if task["task_id"] == task_id:
            return {"status": 200, "time_spent": task["time_spent"]}
    return {"status": 404, "data": "Task not found"}

@app.put("/tasks/{task_id}/time")
def track_time_spent(task_id: int, time_spent: int):
    for task in temp_db:
        if task["task_id"] == task_id:
            task["time_spent"] = time_spent
            return {"status": 200, "data": task}
    return {"status": 404, "data": "Task not found"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
