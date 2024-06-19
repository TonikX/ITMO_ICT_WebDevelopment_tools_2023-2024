# Models
```
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel


class Profession(BaseModel):
    id: int
    title: str
    description: str


class Skill(BaseModel):
    id: int
    name: str
    description: str


class RaceType(Enum):
    director = "director"
    worker = "worker"
    junior = "junior"


class Warrior(BaseModel):
    id: int
    race: RaceType
    name: str
    level: int
    profession: Profession
    skills: Optional[List[Skill]] = []

```

# db.py
```
temp_bd = [
    {
        "id": 1,
        "race": "director",
        "name": "Старовойтова Лиза",
        "level": 12,
        "profession": {
            "id": 2,
            "title": "Старшая сестра",
            "description": "Главная из сестер",
        },
    },
    {
        "id": 2,
        "race": "worker",
        "name": "Старовойтова Катя",
        "level": 12,
        "profession": {
            "id": 1,
            "title": "Младшая сестра",
            "description": "Младше на 5 минут",
        },
    },
]


db_professions = [
    {"id": 1, "title": "Старшая сестра", "description": "Главная из сестер"},
    {
        "id": 2,
        "title": "Младшая сестра",
        "description": "Младше на 5 минут",
    },
]

```

# Main.py
```
import uvicorn
from fastapi import FastAPI, HTTPException

from typing_extensions import List, TypedDict

import db
import models

app = FastAPI()

warior_create_response = TypedDict("Response", {"status": int, "data": models.Warrior})


@app.get("/warriors_list")
def warriors_list() -> List[models.Warrior]:
    return db.temp_bd


@app.get("/warrior/{warrior_id}")
def warriors_get(warrior_id: int) -> List[models.Warrior]:
    return [warrior for warrior in db.temp_bd if warrior.get("id") == warrior_id]


@app.post("/warrior")
def warriors_create(
    warrior: models.Warrior,
) -> warior_create_response:
    warrior_to_append = warrior.model_dump()
    db.temp_bd.append(warrior_to_append)
    return {"status": 200, "data": warrior}


@app.delete("/warrior/delete{warrior_id}")
def warrior_delete(warrior_id: int):
    for i, warrior in enumerate(db.temp_bd):
        if warrior.get("id") == warrior_id:
            db.temp_bd.pop(i)
            break
    return {"status": 201, "message": "deleted"}


@app.put("/warrior{warrior_id}")
def warrior_update(warrior_id: int, warrior: models.Warrior) -> List[models.Warrior]:
    for war in db.temp_bd:
        if war.get("id") == warrior_id:
            warrior_to_append = warrior.model_dump()
            db.temp_bd.remove(war)
            db.temp_bd.append(warrior_to_append)
    return db.temp_bd


@app.post("/professions/")
async def create_profession(profession: models.Profession):
    profession_dict = profession.dict()
    profession_dict["id"] = len(db.db_professions) + 1
    db.db_professions.append(profession_dict)
    return profession_dict


@app.get("/professions/", response_model=List[models.Profession])
async def read_professions():
    return db.db_professions


@app.get("/professions/{profession_id}", response_model=models.Profession)
async def read_profession(profession_id: int):
    for profession in db.db_professions:
        if profession["id"] == profession_id:
            return profession
    raise HTTPException(status_code=404, detail="Profession not found")


@app.put("/professions/{profession_id}")
async def update_profession(profession_id: int, profession: models.Profession):
    for index, prof in enumerate(db.db_professions):
        if prof["id"] == profession_id:
            update_profession_dict = profession.dict()
            update_profession_dict["id"] = profession_id
            db.db_professions[index] = update_profession_dict
            return update_profession_dict
    raise HTTPException(status_code=404, detail="Profession not found")


@app.delete("/professions/{profession_id}")
async def delete_profession(profession_id: int):
    for index, profession in enumerate(db.db_professions):
        if profession["id"] == profession_id:
            del db.db_professions[index]
            return {"message": "Profession deleted successfully"}
    raise HTTPException(status_code=404, detail="Profession not found")


if __name__ == '__main__':
    uvicorn.run('main:app', host="localhost", port=8000, reload=True)

```
