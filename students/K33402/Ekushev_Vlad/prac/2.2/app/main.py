from sqlmodel import Session, select
import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from typing import List, TypedDict
from app import db
from app import models

app = FastAPI()


@app.on_event("startup")
def on_startup():
    db.init_db()


@app.get("/ping")
def ping():
    return "pong"


@app.post("/warrior")
def warriors_create(
    warrior: models.WarriorDefault, session=Depends(db.get_session)
) -> TypedDict("Response", {"status": int, "data": models.Warrior}):
    warrior = models.Warrior.model_validate(warrior)
    session.add(warrior)
    session.commit()
    session.refresh(warrior)
    return {"status": 200, "data": warrior}


@app.get("/warriors_list")
def warriors_list(session=Depends(db.get_session)) -> List[models.Warrior]:
    return session.exec(select(models.Warrior)).all()


@app.get("/warrior/{warrior_id}", response_model=models.WarriorProfessions)
def warriors_get(warrior_id: int, session=Depends(db.get_session)) -> models.Warrior:
    warrior = session.get(models.Warrior, warrior_id)
    return warrior


@app.patch("/warrior/{warrior_id}")
def warrior_update(
    warrior_id: int, warrior: models.WarriorDefault, session=Depends(db.get_session)
) -> models.WarriorDefault:
    db_warrior = session.get(models.Warrior, warrior_id)
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
def warrior_delete(warrior_id: int, session=Depends(db.get_session)):
    warrior = session.get(models.Warrior, warrior_id)
    if not warrior:
        raise HTTPException(status_code=404, detail="Warrior not found")
    session.delete(warrior)
    session.commit()
    return {"ok": True}


@app.get("/professions_list")
def professions_list(session=Depends(db.get_session)) -> List[models.Profession]:
    return session.exec(select(models.Profession)).all()


@app.get("/profession/{profession_id}")
def profession_get(
    profession_id: int, session: Session = Depends(db.get_session)
) -> models.Profession:
    return session.get(models.Profession, profession_id)


@app.post("/profession")
def profession_create(
    prof: models.ProfessionDefault, session: Session = Depends(db.get_session)
) -> TypedDict(
    "Response", {"status": int, "data": models.Profession}
):
    prof = models.Profession.model_validate(prof)
    session.add(prof)
    session.commit()
    session.refresh(prof)
    return {"status": 200, "data": prof}


@app.post("/skills/")
def create_skill(
    skill: models.SkillDefault, session: Session = Depends(db.get_session)
):
    skill = models.Skill.model_validate(skill)
    session.add(skill)
    session.commit()
    session.refresh(skill)
    return {"status": 200, "data": skill}


@app.get("/skills/{skill_id}")
def read_skill(skill_id: int, session: Session = Depends(db.get_session)):
    skill = session.get(models.Skill, skill_id)
    if skill is None:
        raise HTTPException(status_code=404, detail="Skill not found")
    return skill


@app.patch("/skills/{skill_id}")
def update_skill(
    skill_id: int, skill: models.SkillDefault, session: Session = Depends(db.init_db)
):
    db_skill = session.get(models.Skill, skill_id)
    if db_skill is None:
        raise HTTPException(status_code=404, detail="Skill not found")
    skill_data = skill.model_dump(exclude_unset=True)
    for key, value in skill_data.items():
        setattr(db_skill, key, value)
    session.add(db_skill)
    session.commit()
    session.refresh(db_skill)
    return db_skill


@app.delete("/skills/{skill_id}")
def skill_delete(skill_id: int, session: Session = Depends(db.get_session)):
    skill = session.get(models.Skill, skill_id)
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    session.delete(skill)
    session.commit()
    return {"ok": True}


def start():
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
