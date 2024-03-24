from typing import List, Optional

from typing_extensions import TypedDict

from fastapi import FastAPI

from models import Warrior, Profession

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
        "description": "Эксперт по всем вопросам"
    },
    "skills":
        [{
            "id": 1,
            "name": "Купле-продажа компрессоров",
            "description": ""

        },
        {
            "id": 2,
            "name": "Оценка имущества",
            "description": ""

        }]
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
    "skills": []
},
]

professions_db = [
    {"id": 1, "title": "Lead", "description": "Эксперт по всем вопросам"},
    {"id": 2, "title": "Middle", "description": "Сотрудник опытный"},
]


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


@app.delete("/warrior/delete{warrior_id}")
def warrior_delete(warrior_id: int):
    for i, warrior in enumerate(temp_bd):
        if warrior.get("id") == warrior_id:
            temp_bd.pop(i)
            break
    return {"status": 201, "message": "deleted"}


@app.put("/warrior{warrior_id}")
def warrior_update(warrior_id: int, warrior: Warrior) -> List[Warrior]:
    for war in temp_bd:
        if war.get("id") == warrior_id:
            warrior_to_append = warrior.model_dump()
            temp_bd.remove(war)
            temp_bd.append(warrior_to_append)
    return temp_bd


@app.get("/professions/", response_model=List[Profession])
def get_professions():
    return professions_db

@app.get("/professions/{profession_id}", response_model=Optional[Profession])
def get_profession(profession_id: int):
    for profession in professions_db:
        if profession["id"] == profession_id:
            return profession
    return None

@app.post("/professions/", response_model=Profession, status_code=201)
def create_profession(profession: Profession):
    profession_dict = profession.dict()
    profession_dict["id"] = len(professions_db) + 1
    professions_db.append(profession_dict)
    return profession_dict

@app.put("/professions/{profession_id}", response_model=Optional[Profession])
def update_profession(profession_id: int, profession: Profession):
    for i, prof in enumerate(professions_db):
        if prof["id"] == profession_id:
            update_profession_dict = profession.dict()
            professions_db[i] = update_profession_dict
            return update_profession_dict
    return None

@app.delete("/professions/{profession_id}", status_code=204)
def delete_profession(profession_id: int):
    for i, prof in enumerate(professions_db):
        if prof["id"] == profession_id:
            del professions_db[i]
            return {"message": "Profession deleted"}
    return {"message": "Profession not found"}