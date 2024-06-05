# main.py

```
from typing_extensions import TypedDict

import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import select

from connection import init_db, get_session
from models import *
```
```
app = FastAPI()

```
```
@app.post("/warrior")
def warriors_create(warrior: WarriorDefault, session=Depends(get_session)) -> TypedDict(
    'Response', {
        "status": int,
        "data": Warrior
    }
): # type: ignore
    warrior = Warrior.model_validate(warrior)
    session.add(warrior)
    session.commit()
    session.refresh(warrior)
    return {"status": 200, "data": warrior}

```
```
@app.get("/warriors_list")
def warriors_list(session=Depends(get_session)) -> List[Warrior]:
    return session.exec(select(Warrior)).all()
```
```

@app.get("/skills_list")
def skills_list(session=Depends(get_session)) -> List:
    data = session.exec(select(Skill)).all()
    return data
```
```

@app.post("/skills_create")
def skill_create(skill: Skill, session=Depends(get_session)) -> TypedDict(
    'Response',
    {"status": int, "data": Skill}
): # type: ignore
    skill = Skill.model_validate(skill)
    session.add(skill)
    session.commit()
    session.refresh(skill)
    return {"status": 200, "data": skill}
```
```

@app.post("/warrior_adv_skill")
def warrior_adv_skill(row: SkillWarriorLink, session=Depends(get_session)) -> TypedDict(
    'Response', {
        "status": int,
        "data": SkillWarriorLink
    }
): # type: ignore
    row = SkillWarriorLink.model_validate(row)
    session.add(row)
    session.commit()
    session.refresh(row)
    return {"status": 200, "data": row}
```
```

@app.get("/warrior/{warrior_id}", response_model=WarriorDetails)
def warriors_get(warrior_id: int, session=Depends(get_session)):
    warrior = session.get(Warrior, warrior_id)
    return warrior
```
```

@app.delete("/warrior/delete{warrior_id}")
def warrior_delete(warrior_id: int, session=Depends(get_session)):
    warrior = session.get(Warrior, warrior_id)
    if not warrior:
        raise HTTPException(status_code=404, detail="Warrior not found")
    session.delete(warrior)
    session.commit()
    return {"ok": True}
```
```

@app.patch("/warrior{warrior_id}")
def warrior_update(
    warrior_id: int,
    warrior: WarriorDefault,
    session=Depends(get_session)
) -> WarriorDefault:
    db_warrior = session.get(Warrior, warrior_id)
    if not db_warrior:
        raise HTTPException(status_code=404, detail="Warrior not found")
    warrior_data = warrior.model_dump(exclude_unset=True)
    for key, value in warrior_data.items():
        setattr(db_warrior, key, value)
    session.add(db_warrior)
    session.commit()
    session.refresh(db_warrior)
    return db_warrior
```
```

@app.get("/professions_list")
def professions_list(session=Depends(get_session)) -> List[Profession]:
    return session.exec(select(Profession)).all()
```
```

@app.get("/profession/{profession_id}")
def profession_get(profession_id: int, session=Depends(get_session)) -> Profession:
    return session.get(Profession, profession_id)

```
```
@app.post("/profession")
def profession_create(prof: Profession, session=Depends(get_session)) -> TypedDict(
    'Response', {
        "status": int,
        "data": Profession
    }
): # type: ignore
    prof = Profession.model_validate(prof)
    session.add(prof)
    session.commit()
    session.refresh(prof)
    return {"status": 200, "data": prof}

```
```
if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
```