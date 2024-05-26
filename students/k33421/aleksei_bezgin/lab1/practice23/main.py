## что значит "создать api для профессий?"

from typing import Union
from typing_extensions import TypedDict

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import selectinload, joinedload
from sqlmodel import select

from connection import init_db, get_session
from models import *

app = FastAPI()


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/warriors_list")
def warriors_list(session=Depends(get_session)):
    warriors = session.exec(select(Warrior).options(selectinload(Warrior.skills))).all()
    return warriors


@app.get("/warrior/{warrior_id}", response_model=Union[WarriorProfessions, WarriorSkills])
def warrior_get(warrior_id: int, session=Depends(get_session)):
    warrior = session.exec(select(Warrior).options(joinedload(Warrior.skills)).where(Warrior.id == warrior_id)).first()
    if not warrior:
        raise HTTPException(status_code=404, detail="Warrior not found")
    return warrior


@app.delete("/warrior/delete{warrior_id}")
def warrior_delete(warrior_id: int, session=Depends(get_session)):
    warrior = session.get(Warrior, warrior_id)
    if not warrior:
        raise HTTPException(status_code=404, detail="Warrior not found")
    session.delete(warrior)
    session.commit()
    return {"ok": True}


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


@app.post("/warrior")
def warriors_create(warrior: WarriorDefault, session=Depends(get_session)) -> TypedDict('Response', {"status": int,
                                                                                                     "data": Warrior}):
    warrior = Warrior.model_validate(warrior)
    session.add(warrior)
    session.commit()
    session.refresh(warrior)
    return {"status": 200, "data": warrior}


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


## many2many сложно
@app.get("/skills_list")
def skills_list(session=Depends(get_session)) -> List[Skill]:
    return session.exec(select(Skill)).all()


@app.get("/skill/{skill_id}")
def skill_get(skill_id: int, session=Depends(get_session)) -> Skill:
    return session.get(Skill, skill_id)


@app.post("/skill")
def profession_create(skill: SkillDefault, session=Depends(get_session)) -> TypedDict('Response', {"status": int,
                                                                                                   "data": Skill}):
    skill = Skill.model_validate(skill)
    session.add(skill)
    session.commit()
    session.refresh(skill)
    return {"status": 200, "data": skill}


@app.post("/assign_skill_to_warrior")
def assign_skill_to_warrior(warrior_id: int, skill_id: int, session=Depends(get_session)):
    # Check if the warrior and skill exist
    warrior = session.get(Warrior, warrior_id)
    if not warrior:
        raise HTTPException(status_code=404, detail="Warrior not found")

    skill = session.get(Skill, skill_id)
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")

    # Check if the relation already exists
    existing_link = session.exec(select(SkillWarriorLink).where(
        (SkillWarriorLink.skill_id == skill_id) & (SkillWarriorLink.warrior_id == warrior_id)
    )).first()
    if existing_link:
        raise HTTPException(status_code=400, detail="Relation already exists")

    # Create the new relation
    link = SkillWarriorLink(skill_id=skill_id, warrior_id=warrior_id)
    session.add(link)
    session.commit()

    return {"status": 200, "message": "success"}
