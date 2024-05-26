from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, List, TypedDict
from enum import Enum

app = FastAPI()


class RaceType(Enum):
    director = 'director'
    worker = 'worker'
    junior = 'junior'


class Warrior(BaseModel):
    id: int
    race: RaceType
    name: str
    level: int
    profession: "Profession"


class Profession(BaseModel):
    id: int
    title: str
    description: str

temp_bd = [{
    "id": 1,
    "race": "director",
    "name": "Мартынов Дмитрий",
    "level": 12,
    "profession": {
        "id": 1,
        "title": "Влиятельный человек",
        "description": "Эксперт по всем вопросам"
    },
},
    {
        "id": 2,
        "race": "worker",
        "name": "Андрей Косякин",
        "level": 12,
        "profession": {
            "id": 1,
            "title": "Дельфист-гребец",
            "description": "Уважаемый сотрудник"
        },
    },
]


@app.get('/warriors/list')
def get_all_wariors() -> List[Warrior]:
    return temp_bd


@app.get('/warrior/{warrior_id}')
def get_warrior_by_id(warrior_id: int) -> Warrior:
    return [warrior for warrior in temp_bd if warrior.get("id") == warrior_id][0]


@app.post('/warrior/create')
def create_warrior(data: Warrior) -> TypedDict('Response', {'status': int, 'data': Warrior}): # Тип входных данны надо обязательно указывать, инач
    return {"status": 200, "data": data} # "status" по приколу пишем, он просто в json попадает. На статус ответа не влияет


@app.post('/profession/create')
# data автоматически проверяется pydantic и если чего-то нет, то ошибка
def create_warrior(data: Profession) -> TypedDict('Response', {'status': int, 'data': Profession}): # Тип входных данны надо обязательно указывать, инач
    return {"status": 200, "data": data} # "status" по приколу пишем, он просто в json попадает. На статус ответа не влияет


@app.delete('/warrior/delete/{warrior_id}')
def delete_warrior(warrior_id):
    # return None # просто вернет null и все
    return {"status": 201, "message": 'hello world'} # все равно будет 201 статус



@app.put('/warrior/put/{warrior_id}')
def put_warriot(warrior_id: int, data: dict):
    return temp_bd