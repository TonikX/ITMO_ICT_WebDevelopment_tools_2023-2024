# main.py


```
from typing import TypedDict
from fastapi import FastAPI
from models import *
```
```
app = FastAPI()
```
```
@app.get("/")
def hello():
    return "Hello, [username]!"
```
```
warriors_temp = [{
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
            "id": 2,
            "title": "Дельфист-гребец",
            "description": "Уважаемый сотрудник"
        }
    }
]
```
```
professions_temp = [{
  "id": 1,
  "title": "Влиятельный человек",
  "description": "Эксперт по всем вопросам"
},
{
  "id": 2,
  "title": "Дельфист-гребец",
  "description": "Уважаемый сотрудник"
},
]

```
```
@app.get("/warriors_list")
def warriors_list() -> List[Warrior]:
    return warriors_temp
```
```
@app.get("/warrior/{warrior_id}")
def warriors_get(warrior_id: int) -> List[Warrior]:
    return [warrior for warrior in warriors_temp if warrior.get("id") == warrior_id]
```
```
@app.post("/warrior")
def warriors_create(warrior: Warrior) -> TypedDict('Response', {"status": int, "data": Warrior}):
    warrior_to_append = warrior.model_dump()
    warriors_temp.append(warrior_to_append)
    return {"status": 200, "data": warrior}
```
```
@app.delete("/warrior/delete{warrior_id}")
def warrior_delete(warrior_id: int):
    for i, warrior in enumerate(warriors_temp):
        if warrior.get("id") == warrior_id:
            warriors_temp.pop(i)
            break
    return {"status": 201, "message": "deleted"}
```
```
@app.put("/warrior{warrior_id}")
def warrior_update(warrior_id: int, warrior: Warrior) -> List[Warrior]:
    for war in warriors_temp:
        if war.get("id") == warrior_id:
            warrior_to_append = warrior.model_dump()
            warriors_temp.remove(war)
            warriors_temp.append(warrior_to_append)
    return warriors_temp
```
```
@app.get("/profession_list")
def profession_list() -> List[Profession]:
    return professions_temp
```
```
@app.get("/profession/{profession_id}")
def warriors_get(profession_id: int) -> List[Profession]:
    return [profession for profession in professions_temp if profession.get("id") == profession_id]
```
```
@app.post("/profession")
def profession_create(profession: Profession) -> TypedDict('Response', {"status": int, "data": Profession}):
    profession_to_append = profession.model_dump()
    professions_temp.append(profession_to_append)
    return {"status": 200, "data": profession}
```
```
@app.delete("/profession/delete{profession_id}")
def profession_delete(profession_id: int):
    for i, profession in enumerate(professions_temp):
        if profession.get("id") == profession_id:
            professions_temp.pop(i)
            break
    return {"status": 201, "message": "deleted"}
```
```
@app.put("/profession{profession_id}")
def profession_update(profession_id: int, profession: Profession) -> List[Profession]:
    for prof in professions_temp:
        if prof.get("id") == profession_id:
            profession_to_append = profession.model_dump()
            professions_temp.remove(prof)
            professions_temp.append(profession_to_append)
    return professions_temp
```