from typing import List
from fastapi import FastAPI
from models import Warrior
from typing_extensions import TypedDict

app = FastAPI()

temp_bd = [{
    "id": 1,
    "race": "director",
    "name": "Николай Соболев",
    "level": 100,
    "profession": {
        "id": 1,
        "title": "Директор по модерационной политике",
        "description": "Модерирует контент"
    },
    "skills": [{"id": 13, "name": "Ночное видение", "description": "Видит ночью"}]
},
    {
        "id": 2,
        "race": "worker",
        "name": "Александр Соболев",
        "level": 1,
        "profession": {
            "id": 121,
            "title": "Младший разработчик контента",
            "description": "Самый молодой сотрудник в штате"
        },
    },
    {
        "id": 3,
        "race": "junior",
        "name": "Максим Соболев",
        "level": 12,
        "profession": {
            "id": 12,
            "title": "Стажер команды ios разработки",
            "description": "ios разработчик без опыта"
        },
    },
]


@app.get("/")
def hello():
    return "Hello, User!"


@app.get("/warriors_list")
def warriors_list() -> List[Warrior]:
    return temp_bd


@app.get("/warrior/{warrior_id}")
def warriors_get(warrior_id: int) -> List[Warrior]:
    return [warrior for warrior in temp_bd if warrior.get("id") == warrior_id]


@app.post("/warrior")
def warriors_create(warrior: Warrior) -> TypedDict('Response', {"status": int, "data": Warrior}):
    warrior_to_append = warrior.model_dump()
    temp_bd.append(warrior_to_append)
    return {"status": 200, "data": warrior}


@app.delete("/warrior/delete/{warrior_id}")
def warrior_delete(warrior_id: int):
    for index, warrior in enumerate(temp_bd):
        if warrior.get("id") == warrior_id:
            temp_bd.pop(index)
            break
    return {"status": 200, "message": "deleted"}


@app.put("/warrior/{warrior_id}")
def warrior_update(warrior_id: int, warrior: Warrior) -> List[Warrior]:
    for war in temp_bd:
        if war.get("id") == warrior_id:
            warrior_to_append = warrior.model_dump()
            temp_bd.remove(war)
            temp_bd.append(warrior_to_append)
    return temp_bd