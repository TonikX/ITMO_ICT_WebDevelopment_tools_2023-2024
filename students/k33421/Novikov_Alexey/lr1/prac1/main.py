import datetime

from fastapi import FastAPI

from lab1.prac1.models import Task, TaskWithLinks, Message, Data, Sprint

temp_bd = [
    {
        "id": 1,
        "summary": "Do something",
        "priority": "trivial",
        "description": "Do something",
        "planned_end_at": datetime.datetime(hour=10, minute=0, second=0, day=10, month=1, year=2024),
        "status": "open",
        "created_at": datetime.datetime(hour=10, minute=0, second=0, day=5, month=1, year=2024),
        "updated_at": datetime.datetime(hour=10, minute=0, second=0, day=5, month=1, year=2024),
        "sprint": {
            "id": 1,
            "title": "Sprint1",
            "start_at": datetime.datetime(hour=10, minute=0, second=0, day=1, month=1, year=2024),
            "end_at": datetime.datetime(hour=10, minute=0, second=0, day=14, month=1, year=2024),
        },
        "linked_tasks": [
            {
                "task": {
                    "id": 2,
                    "summary": "Do something other",
                    "priority": "major",
                    "description": "Do something other",
                    "planned_end_at": datetime.datetime(hour=10, minute=0, second=0, day=10, month=1, year=2024),
                    "status": "in_progress",
                    "created_at": datetime.datetime(hour=10, minute=0, second=0, day=5, month=1, year=2024),
                    "updated_at": datetime.datetime(hour=10, minute=0, second=0, day=5, month=1, year=2024),
                    "sprint": {
                        "id": 2,
                        "title": "Sprint2",
                        "start_at": datetime.datetime(hour=10, minute=0, second=0, day=1, month=1, year=2024),
                        "end_at": datetime.datetime(hour=10, minute=0, second=0, day=14, month=1, year=2024),
                    },
                },
                "status": "is_blocked_by",
            }
        ],
    },
    {
        "id": 2,
        "summary": "Do something other",
        "priority": "major",
        "description": "Do something other",
        "planned_end_at": datetime.datetime(hour=10, minute=0, second=0, day=10, month=1, year=2024),
        "status": "in_progress",
        "created_at": datetime.datetime(hour=10, minute=0, second=0, day=5, month=1, year=2024),
        "updated_at": datetime.datetime(hour=10, minute=0, second=0, day=5, month=1, year=2024),
        "sprint": {
            "id": 2,
            "title": "Sprint2",
            "start_at": datetime.datetime(hour=10, minute=0, second=0, day=1, month=1, year=2024),
            "end_at": datetime.datetime(hour=10, minute=0, second=0, day=14, month=1, year=2024),
        },
        "linked_tasks": [],
    },
]

app = FastAPI()


@app.get("/tasks")
def get_tasks() -> list[TaskWithLinks]:
    return [TaskWithLinks(**task) for task in temp_bd]


@app.get("/tasks/{task_id}")
def get_task(task_id: int) -> TaskWithLinks | None:
    for task in temp_bd:
        if task.get("id") == task_id:
            return TaskWithLinks(**task)
    else:
        return None


@app.post("/tasks")
def add_task(task: Task, sprint: Sprint | None = None) -> Data:
    created_task = task.model_dump()

    if sprint:
        created_task["sprint"] = sprint.model_dump()

    temp_bd.append(created_task)
    return Data(status=200, data=Task(**created_task))


@app.delete("/tasks/{task_id}", status_code=201)
def delete_task(task_id: int) -> Message:
    for i, task in enumerate(temp_bd):
        if task.get("id") == task_id:
            temp_bd.pop(i)
            break

    return Message(status=201, message="deleted")


@app.put("/tasks/{task_id}")
def update_task(task_id: int, task_data: Task) -> Task:
    for task in temp_bd:
        if task.get("id") == task_id:
            temp_bd.remove(task)
            temp_bd.append(task_data.model_dump())
            return task_data
