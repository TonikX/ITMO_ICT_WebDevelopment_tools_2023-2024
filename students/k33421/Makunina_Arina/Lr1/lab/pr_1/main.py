from fastapi import FastAPI, HTTPException

from models import *

app = FastAPI()


@app.get("/")
def hello():
    return "Hello, arina!"


temp_db_tasks = [
    {
        "id": 1,
        "title": "Задача 1",
        "description": "Описание задачи 1",
        "deadline": datetime(2023, 4, 30, 17, 0, 0),
        "priority": PriorityLevel.HIGH,
        "time_spent": 1.5,
    },
    {
        "id": 2,
        "title": "Задача 2",
        "description": "Описание задачи 2",
        "deadline": datetime(2023, 5, 5, 12, 0, 0),
        "priority": PriorityLevel.MEDIUM,
        "time_spent": 2.0,
    },
]

temp_db_schedule = [{"date": datetime(2023, 4, 30), "tasks": [1, 2]}]


@app.get("/tasks", response_model=List[TaskResponse])
def get_tasks() -> List[TaskResponse]:
    return [TaskResponse(**task) for task in temp_db_tasks]


@app.post("/tasks", response_model=TaskResponse)
def create_task(task: CreateTask) -> TaskResponse:
    new_task = task.dict()
    new_task["id"] = len(temp_db_tasks) + 1
    temp_db_tasks.append(new_task)
    return TaskResponse(**new_task)


@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task_update: UpdateTask) -> TaskResponse:
    for task in temp_db_tasks:
        if task["id"] == task_id:
            task_data = task.copy()
            task_data.update(task_update.dict(exclude_unset=True))
            return TaskResponse(**task_data)
    raise HTTPException(status_code=404, detail="Task not found")


@app.delete("/tasks/{task_id}", response_model=dict)
def delete_task(task_id: int) -> dict:
    global temp_db_tasks
    temp_db_tasks = [task for task in temp_db_tasks if task["id"] != task_id]
    return {"message": "Task deleted"}
