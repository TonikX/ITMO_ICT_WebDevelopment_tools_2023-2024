from fastapi import FastAPI, Body, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import Optional, List
from models import (
    Warrior,
    Profession,
    RaceType,
    WarriorProfessions,
    WarriorDefault,
    Skill,
    SkillWarriorLink,
)
from connection import init_db, get_session

app = FastAPI()


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/")
def hello():
    return "Hello, [username]!"


@app.post("/warrior", response_model=Warrior)
def create_warrior(
    warrior: WarriorDefault,
    session: Session = Depends(get_session),
):

    warrior = Warrior.model_validate(warrior)
    session.add(warrior)
    session.commit()
    session.refresh(warrior)
    return warrior


@app.get("/warrior/{warrior_id}", response_model=WarriorProfessions)
async def get_warrior_skills(warrior_id: int, db: Session = Depends(get_session)):
    warrior = db.query(Warrior).filter(Warrior.id == warrior_id).first()
    if not warrior:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Warrior not found"
        )

    skills = (
        db.query(Skill)
        .join(SkillWarriorLink, SkillWarriorLink.skill_id == Skill.id)
        .filter(SkillWarriorLink.warrior_id == warrior_id)
        .all()
    )

    warrior.skills = skills
    return warrior


@app.get("/warrior_list", response_model=List[Warrior])
def warriors_list(session=Depends(get_session)) -> List[Warrior]:
    return session.query(Warrior).all()


@app.put("/warrior/put/{warrior_id}", response_model=Warrior)
def update_warrior(
    warrior_id: int, warrior: Warrior, session: Session = Depends(get_session)
):
    db_warrior = session.get(Warrior, warrior_id)
    if db_warrior is None:
        raise HTTPException(status_code=404, detail="Warrior not found")
    db_warrior.name = warrior.name
    db_warrior.race = RaceType(warrior.race)
    db_warrior.level = warrior.level
    db_warrior.profession_id = warrior.profession_id
    session.commit()
    return db_warrior


@app.delete("/warrior/delete/{warrior_id}")
def delete_warrior(warrior_id: int, session: Session = Depends(get_session)):
    warrior = session.get(Warrior, warrior_id)
    if warrior is None:
        raise HTTPException(status_code=404, detail="Warrior not found")
    session.delete(warrior)
    session.commit()
    return {"status": "successful"}


@app.post("/profession")
def profession_create(title: str, description: str, session=Depends(get_session)):
    prof = Profession(title=title, description=description)
    session.add(prof)
    session.commit()
    session.refresh(prof)
    return {"status": 200, "data": prof}


@app.post("/warriors/addskills/{warrior_id}/")
async def add_skill_to_warrior(
    warrior_id: int, skill_name: str = Body(...), db: Session = Depends(get_session)
):
    warrior = db.query(Warrior).filter(Warrior.id == warrior_id).first()
    if not warrior:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Warrior not found"
        )

    existing_skill = db.query(Skill).filter(Skill.name == skill_name).first()
    if not existing_skill:
        new_skill = Skill(name=skill_name)
        db.add(new_skill)
        db.commit()
        existing_skill = new_skill
    else:
        if any(skill.id == existing_skill.id for skill in warrior.skills):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Warrior already has this skill",
            )

    link = SkillWarriorLink(warrior_id=warrior.id, skill_id=existing_skill.id)
    db.add(link)
    db.commit()

    return {"message": "Skill added successfully"}


@app.put("/warriors/{warrior_id}/skills/{skill_id}")
async def modify_warrior_skill(
    warrior_id: int,
    skill_id: int,
    new_skill_name: str = Body(...),
    db: Session = Depends(get_session),
):
    warrior = db.query(Warrior).filter(Warrior.id == warrior_id).first()
    if not warrior:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Warrior not found"
        )

    existing_skill_link = (
        db.query(SkillWarriorLink)
        .filter(
            SkillWarriorLink.warrior_id == warrior_id,
            SkillWarriorLink.skill_id == skill_id,
        )
        .first()
    )
    if not existing_skill_link:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Skill association not found"
        )

    existing_skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if not existing_skill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Skill not found"
        )

    if new_skill_name:
        existing_skill.name = new_skill_name
        db.commit()

    return {"message": "Skill association modified successfully"}


@app.get("/profession/{profession_id}", response_model=Profession)
def read_profession(profession_id: int, session: Session = Depends(get_session)):
    profession = session.get(Profession, profession_id)
    if profession is None:
        raise HTTPException(status_code=404, detail="Profession not found")
    return profession


@app.get("/profession_list", response_model=List[Profession])
def professions_list(session=Depends(get_session)) -> List[Profession]:
    return session.query(Profession).all()


@app.put("/profession/{profession_id}", response_model=Profession)
def update_profession(
    profession_id: int, profession: Profession, session: Session = Depends(get_session)
):
    db_profession = session.get(Profession, profession_id)
    if db_profession is None:
        raise HTTPException(status_code=404, detail="Profession not found")
    db_profession.title = profession.title
    db_profession.description = profession.description
    session.commit()
    return db_profession


@app.delete("/profession/{profession_id}")
def delete_profession(profession_id: int, session: Session = Depends(get_session)):
    profession = session.get(Profession, profession_id)
    if profession is None:
        raise HTTPException(status_code=404, detail="Profession not found")
    session.delete(profession)
    session.commit()
    return {"status": "successful"}


@app.get("/clear_db")
def clear_db(session: Session = Depends(get_session)):
    num_deleted = session.query(Warrior).delete()
    session.query(Profession).delete()
    session.commit()
    return {"status": "successful", "num_deleted": num_deleted}
