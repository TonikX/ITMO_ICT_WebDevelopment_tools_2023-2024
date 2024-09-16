from fastapi import FastAPI

from typing import Optional, List
from typing_extensions import TypedDict
from models import Warrior, Profession, Skill

app = FastAPI()

temp_bd = [
    {
        "id": 1,
        "race": "director",
        "name": "Мартынов Дмитрий",
        "level": 12,
        "profession": {
            "id": 1,
            "title": "Влиятельный человек",
            "description": "Эксперт по всем вопросам",
        },
        "skills": [
            {"id": 1, "name": "Купле-продажа компрессоров", "description": ""},
            {"id": 2, "name": "Оценка имущества", "description": ""},
        ],
    },
    {
        "id": 2,
        "race": "worker",
        "name": "Андрей Косякин",
        "level": 12,
        "profession": {
            "id": 2,
            "title": "Дельфист-гребец",
            "description": "Уважаемый сотрудник",
        },
        "skills": [],
    },
    {
        "id": 3,
        "race": "worker",
        "name": "Max",
        "level": 4,
        "profession": {"id": 3, "title": "Miner", "description": "Hard Work"},
        "skills": [],
    },
]


@app.get("/")
def hello():
    return "Hello, [username]!"


@app.get("/warriors_list")
def warriors_list() -> List[Warrior]:
    return temp_bd


@app.get("/warrior/{warrior_id}")
def warriors_get(warrior_id: int) -> List[Warrior]:
    return [warrior for warrior in temp_bd if warrior.get("id") == warrior_id]


@app.get("/profession_list")
def profession_list() -> List[Profession]:
    return [warrior.get("profession") for warrior in temp_bd]


@app.get("/profession/{warrior_id}")
def profession_get(warrior_id: int) -> List[Profession]:
    return [
        warrior.get("profession")
        for warrior in temp_bd
        if warrior.get("id") == warrior_id
    ]


@app.post("/warrior")
def warriors_create(
    warrior: Warrior,
) -> TypedDict("Response", {"status": int, "data": Warrior}):  # type: ignore
    warrior_to_append = warrior.dict()
    temp_bd.append(warrior_to_append)
    return {"status": 200, "data": warrior}


@app.delete("/warrior/delete/{warrior_id}")
def warrior_delete(warrior_id: int):
    for i, warrior in enumerate(temp_bd):
        if warrior.get("id") == warrior_id:
            temp_bd.pop(i)
            break
    return {"status": 201, "message": "deleted"}


@app.put("/warrior/update/{warrior_id}")
def warrior_update(warrior_id: int, warrior: Warrior) -> List[Warrior]:
    for war in temp_bd:
        if war.get("id") == warrior_id:
            warrior_to_append = warrior.model_dump()
            temp_bd.remove(war)
            temp_bd.append(warrior_to_append)
    return temp_bd
