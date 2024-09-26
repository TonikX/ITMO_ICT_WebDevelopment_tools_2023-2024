from fastapi import FastAPI, Depends, HTTPException
from typing_extensions import TypedDict
from typing import List
from sqlmodel import select

from connection import init_db, get_session
from models.models import Warrior, WarriorDefault, ProfessionDefault, Profession, WarriorProfessions, Skill, SkillDefault, SkillWarriorLink

app = FastAPI()


@app.on_event("startup")
def on_startup():
    init_db()


@app.post("/warrior")
def warriors_create(warrior: WarriorDefault, session=Depends(get_session)) -> TypedDict('Response', {"status": int, "data": Warrior}):
    warrior = Warrior.model_validate(warrior)
    session.add(warrior)
    session.commit()
    session.refresh(warrior)
    return {"status": 200, "data": warrior}


@app.get("/warriors_list")
def warriors_list(session=Depends(get_session)) -> List[Warrior]:
    return session.exec(select(Warrior)).all()


@app.get("/warrior/{warrior_id}", response_model=WarriorProfessions)
def warriors_get(warrior_id: int, session=Depends(get_session)) -> Warrior:
    return session.get(Warrior, warrior_id)


@app.patch("/warrior{warrior_id}")
def warrior_update(warrior_id: int, warrior: WarriorDefault, session=Depends(get_session)) -> Warrior:
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


@app.get("/professions_list")
def professions_list(session=Depends(get_session)) -> List[Profession]:
    return session.exec(select(Profession)).all()


@app.get("/profession/{profession_id}")
def profession_get(profession_id: int, session=Depends(get_session)) -> Profession:
    return session.get(Profession, profession_id)


@app.post("/profession")
def profession_create(prof: ProfessionDefault, session=Depends(get_session)) -> TypedDict('Response', {"status": int, "data": Profession}):
    prof = Profession.model_validate(prof)
    session.add(prof)
    session.commit()
    session.refresh(prof)
    return {"status": 200, "data": prof}


@app.get("/skills_list")
def skills_list(session=Depends(get_session)) -> List[Skill]:
    return session.exec(select(Skill)).all()


@app.get("/skills/{skill_id}")
def skill_get(skill_id: int, session=Depends(get_session)) -> Skill:
    return session.get(Skill, skill_id)


@app.post('/skill')
def skill_create(skill: SkillDefault, session=Depends(get_session)) -> TypedDict('Response', {"status": int, "data": Skill}):
    skill = Skill.model_validate(skill)
    session.add(skill)
    session.commit()
    session.refresh(skill)
    return {"status": 200, "data": skill}


@app.patch('/skill/{skill_id}')
def skill_update(skill_id: int, skill: SkillDefault, session=Depends(get_session)) -> Skill:
    db_skill = session.get(Skill, skill_id)
    if not db_skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    skill_data = skill.model_dump(exclude_unset=True)
    for key, value in skill_data.items():
        setattr(db_skill, key, value)
    session.add(db_skill)
    session.commit()
    session.refresh(db_skill)
    return db_skill


@app.delete("/skill/delete{skill_id}")
def skill_delete(skill_id: int, session=Depends(get_session)):
    skill = session.get(Skill, skill_id)
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    session.delete(skill)
    session.commit()
    return {"ok": True}


@app.get("/skillwarriorlink_list")
def skillwarriorlink_list(session=Depends(get_session)) -> List[SkillWarriorLink]:
    return session.exec(select(SkillWarriorLink)).all()


@app.get("/skillwarriorlink/{skill_id}/{warrior_id}")
def skillwarriorlink_get(skill_id: int, warrior_id: int, session=Depends(get_session)) -> SkillWarriorLink:
    return session.get(SkillWarriorLink, (skill_id, warrior_id))


@app.post('/skillwarriorlink')
def skillwarriorlink_create(skillwarriorlink: SkillWarriorLink, session=Depends(get_session)) -> TypedDict('Response', {"status": int, "data": SkillWarriorLink}):
    session.add(skillwarriorlink)
    session.commit()
    session.refresh(skillwarriorlink)
    return {"status": 200, "data": skillwarriorlink}