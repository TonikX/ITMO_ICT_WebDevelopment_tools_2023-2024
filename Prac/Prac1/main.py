from fastapi import FastAPI, HTTPException
from models import Task, Priority, Status, Category, Note
from typing import List
from datetime import date

app = FastAPI()

# Временная база данных для задач
tasks_db = [
    {
        "id": 1,
        "title": "Разработать FastAPI приложение",
        "description": "Создать серверное приложение для тайм-менеджмента",
        "deadline": date(2024, 9, 25),
        "created_date": date(2024, 9, 18),
        "priority": Priority.high,
        "status": Status.in_progress,
        "category": {
            "id": 1,
            "title": "Разработка",
            "description": "Все задачи, связанные с разработкой"
        },
        "notes": [
            {"id": 1, "content": "Настроить виртуальное окружение", "created_at": date(2024, 9, 18)},
            {"id": 2, "content": "Реализовать модели данных", "created_at": date(2024, 9, 19)},
        ]
    },
    {
        "id": 2,
        "title": "Подготовить отчёт по проекту",
        "description": "Написать финальный отчёт и отправить клиенту",
        "deadline": date(2024, 9, 30),
        "created_date": date(2024, 9, 18),
        "priority": Priority.medium,
        "status": Status.to_do,
        "category": {
            "id": 2,
            "title": "Документация",
            "description": "Задачи, связанные с созданием документации"
        },
        "notes": [
            {"id": 1, "content": "Собрать все материалы", "created_at": date(2024, 9, 18)},
            {"id": 2, "content": "Создать структуру отчёта", "created_at": date(2024, 9, 19)},
        ]
    }
]


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
