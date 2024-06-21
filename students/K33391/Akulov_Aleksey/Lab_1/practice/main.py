from http.client import HTTPException

from typing import List, Optional
from typing_extensions import TypedDict

from fastapi import FastAPI, Depends
from sqlmodel import Session, select

from models import Warrior, Profession, WarriorDefault, ProfessionDefault, \
    Skill, SkillDefault
from connections import init_db, get_session

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


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/warriors_list")
def warriors_list(session=Depends(get_session)) -> List[Warrior]:
    return session.exec(select(Warrior)).all()


@app.get("/warrior/{warrior_id}")
def warriors_get(warrior_id: int, session=Depends(get_session)) -> Warrior:
    return session.exec(select(Warrior).where(Warrior.id == warrior_id)).first()


@app.post("/warrior")
def warriors_create(warrior: WarriorDefault, session=Depends(get_session)) -> TypedDict('Response', {"status": int,
                                                                                                     "data": Warrior}):
    warrior = Warrior.model_validate(warrior)
    session.add(warrior)
    session.commit()
    session.refresh(warrior)
    return {"status": 200, "data": warrior}


@app.delete("/warrior/delete{warrior_id}")
def warrior_delete(warrior_id: int):
    for i, warrior in enumerate(temp_bd):
        if warrior.get("id") == warrior_id:
            temp_bd.pop(i)
            break
    return {"status": 201, "message": "deleted"}


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


@app.post("/skills/")
def create_skill(
    skill: SkillDefault, session: Session = Depends(get_session)
):
    skill = Skill.model_validate(skill)
    session.add(skill)
    session.commit()
    session.refresh(skill)
    return {"status": 200, "data": skill}


@app.get("/skills/{skill_id}")
def read_skill(skill_id: int, session: Session = Depends(get_session)):
    skill = session.get(Skill, skill_id)
    if skill is None:
        raise HTTPException(status_code=404, detail="Skill not found")
    return skill


@app.patch("/skills/{skill_id}")
def update_skill(
    skill_id: int, skill: SkillDefault, session: Session = Depends(init_db)
):
    db_skill = session.get(Skill, skill_id)
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
def skill_delete(skill_id: int, session: Session = Depends(get_session)):
    skill = session.get(Skill, skill_id)
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    session.delete(skill)
    session.commit()
    return {"ok": True}