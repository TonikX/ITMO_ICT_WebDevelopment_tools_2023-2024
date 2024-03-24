from datetime import date
from typing import List

from fastapi import FastAPI, HTTPException
from typing_extensions import TypedDict

from models import Category, Task, Note


app = FastAPI()

temp_bd = [
    {
        "id": 1,
        "title": "Лабораторная работа №1",
        "description": "Сделать первую лабораторную работу по веб-програмиированию",
        "deadline": date(2024, 3, 18),
        "priority": "High",
        "status": "In progress",
        "category": {
            "id": 1,
            "title": "Учеба",
            "description": "Задачи для университета"
        },
        "notes":
            [{
                "id": 1,
                "content": "Разработайте простую программу-тайм-менеджер, которая "
                           "поможет управлять вашим временем и задачами. Программа "
                           "должна позволять создавать задачи с описанием, устанавливать "
                           "им сроки выполнения и приоритеты, а также отслеживать "
                           "затраченное время на каждую задачу.",

            },
                {
                    "id": 2,
                    "content": "Дополнительные функции могут включать в себя уведомления о "
                               "приближении к дедлайнам, возможность создания ежедневного "
                               "расписания работы и анализ времени, затраченного на различные задачи.",
                }]
    },
    {
        "id": 2,
        "title": "Сделать уборку",
        "description": "Убраться в квартире",
        "deadline": date.today(),
        "priority": "Medium",
        "status": "To do",
        "category": {
            "id": 2,
            "title": "Дом",
            "description": "Дела по дому"
        },
        "notes":
            [{
                "id": 1,
                "content": "Не забыть разобрать вещи с приезда",
            }]
    }
]


@app.get("/")
async def root():
    return {"message": "Hello World"}


# Эндпоинты для задач
@app.get("/tasks")
async def get_tasks_list():
    return temp_bd


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    return [task for task in temp_bd if task.get("id") == task_id]


@app.post("/task")
def create_task(task: Task) -> TypedDict('Response', {"status": int, "data": Task}):
    task_to_append = task.model_dump()
    temp_bd.append(task_to_append)
    return {"status": 200, "data": task}


@app.delete("/task/{task_id}")
def delete_task(task_id: int):
    for i, task in enumerate(temp_bd):
        if task.get("id") == task_id:
            temp_bd.pop(i)
            return {"status": "success", "message": "Task deleted"}
    raise HTTPException(status_code=404, detail="Task not found")


@app.put("/task/{task_id}")
def update_task(task_id: int, task: Task):
    for i, tsk in enumerate(temp_bd):
        if task.get("id") == task_id:
            task_to_append = task.model_dump()
            temp_bd.remove(tsk)
            temp_bd.append(task_to_append)
            return task_to_append
    raise HTTPException(status_code=404, detail="Task not found")


db_categories = [
    {
        "id": 1,
        "title": "Учеба",
        "description": "Задачи для университета"},
    {
        "id": 2,
        "title": "Дом",
        "description": "Дела по дому"
    }
]


@app.get("/categories", response_model=List[Category])
def get_categories():
    return db_categories


@app.get("/categories/{category_id}")
def get_category(category_id: int):
    return [category for category in db_categories if category.get("id") == category_id]


@app.post("/category")
def create_category(category: Category) -> TypedDict('Response', {"status": int, "data": Category}):
    category_to_append = category.model_dump()
    db_categories.append(category_to_append)
    return {"status": 200, "data": category}


@app.delete("/category/{category_id}")
def delete_category(category_id: int):
    for i, category in enumerate(db_categories):
        if category.get("id") == category_id:
            db_categories.pop(i)
            return {"status": "success", "message": "Category deleted"}
    raise HTTPException(status_code=404, detail="Category not found")


@app.put("/category/{category_id}", response_model=Category)
def update_category(category_id: int, category: Category):
    for i, cat in enumerate(db_categories):
        if cat.get("id") == category_id:
            category_to_append = category.model_dump()
            db_categories.remove(cat)
            db_categories.append(category_to_append)
            return category
    raise HTTPException(status_code=404, detail="Category not found")
