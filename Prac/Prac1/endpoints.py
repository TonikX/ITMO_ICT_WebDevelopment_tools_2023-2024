from fastapi import FastAPI, HTTPException
from models import Task, Priority, Status, Category, Note
from typing import List
from datetime import date

# Эндпоинт для получения всех задач, аннотируем возвращаемый результат как List[Task]
@app.get("/tasks", response_model=List[Task])
def get_tasks():
    return tasks_db


# Эндпоинт для получения конкретной задачи, аннотируем возвращаемый результат как Task
@app.get("/task/{task_id}", response_model=Task)
def get_task(task_id: int):
    task = next((task for task in tasks_db if task["id"] == task_id), None)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


# Эндпоинт для создания новой задачи, аннотируем тело запроса как Task
@app.post("/task", response_model=Task)
def create_task(task: Task):
    tasks_db.append(task.dict())
    return task


# Эндпоинт для обновления задачи, аннотируем тело запроса как Task
@app.put("/task/{task_id}", response_model=Task)
def update_task(task_id: int, updated_task: Task):
    task = next((task for task in tasks_db if task["id"] == task_id), None)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    task_index = tasks_db.index(task)
    tasks_db[task_index] = updated_task.dict()
    return updated_task


# Эндпоинт для удаления задачи, возвращаем статус операции
@app.delete("/task/{task_id}", response_model=dict)
def delete_task(task_id: int):
    task = next((task for task in tasks_db if task["id"] == task_id), None)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    tasks_db.remove(task)
    return {"status": "Task deleted successfully"}