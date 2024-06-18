import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import select
from typing_extensions import List, TypedDict

from connection import init_db, get_session
from models import Warrior, WarriorDefault, WarriorProfessions, ProfessionDefault, Profession, Skill, \
    SkillWarriorLink

app = FastAPI()

app.add_event_handler("startup", init_db)


@app.get("/")
def hello():
    return "Hello, [username]!"


@app.get("/warriors_list")
def warriors_list(session=Depends(get_session)) -> List[Warrior]:
    return session.exec(select(Warrior)).all()


@app.get("/warrior/{warrior_id}", response_model=Warrior)
def get_warrior_with_skills(warrior_id: int, session=Depends(get_session)) -> Warrior:
    warrior = session.exec(select(Warrior).where(Warrior.id == warrior_id)).first()
    if not warrior:
        raise HTTPException(status_code=404, detail="Warrior not found")
    return warrior


@app.post("/warrior")
def warriors_create(warrior: WarriorDefault, session=Depends(get_session)) -> TypedDict('Response', {"status": int,
                                                                                                     "data": Warrior}):
    warrior = Warrior.model_validate(warrior)
    session.add(warrior)
    session.commit()
    session.refresh(warrior)
    return {"status": 200, "data": warrior}


@app.patch("/warrior{warrior_id}")
def warrior_update(warrior_id: int, warrior: WarriorDefault, session=Depends(get_session)) -> WarriorDefault:
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


@app.delete("/warrior/delete{warrior_id}")
def warrior_delete(warrior_id: int, session=Depends(get_session)):
    warrior = session.get(Warrior, warrior_id)
    if not warrior:
        raise HTTPException(status_code=404, detail="Warrior not found")
    session.delete(warrior)
    session.commit()
    return {"ok": True}


# Professions _________________________________________________________________________________________________

@app.get("/professions_list")
def professions_list(session=Depends(get_session)) -> List[Profession]:
    return session.exec(select(Profession)).all()


@app.get("/profession/{profession_id}")
def profession_get(profession_id: int, session=Depends(get_session)) -> Profession:
    return session.get(Profession, profession_id)


@app.post("/profession")
def profession_create(prof: ProfessionDefault, session=Depends(get_session)) -> TypedDict('Response', {"status": int,
                                                                                                       "data": Profession}):
    prof = Profession.model_validate(prof)
    session.add(prof)
    session.commit()
    session.refresh(prof)
    return {"status": 200, "data": prof}


# Skills ________________________________________________________________________________________________________
@app.post("/skill")
def create_skill(skill: Skill, session=Depends(get_session)) -> Skill:
    session.add(skill)
    session.commit()
    session.refresh(skill)
    return skill


@app.get("/skills")
def list_skills(session=Depends(get_session)) -> List[Skill]:
    skills = session.exec(select(Skill)).all()
    return skills


@app.post("/warrior/{warrior_id}/add-skill/{skill_id}")
def add_skill_to_warrior(warrior_id: int, skill_id: int, session=Depends(get_session)):
    link = SkillWarriorLink(warrior_id=warrior_id, skill_id=skill_id)
    session.add(link)
    session.commit()
    return {"status": "Skill added to warrior"}


if __name__ == '__main__':
    uvicorn.run('main:app', host="localhost", port=8000, reload=True)
