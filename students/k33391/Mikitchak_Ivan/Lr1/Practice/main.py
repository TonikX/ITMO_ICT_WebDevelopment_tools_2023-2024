from fastapi import Depends, FastAPI, HTTPException
from typing import List
from sqlmodel import select
from typing_extensions import TypedDict
from contextlib import asynccontextmanager
from connection import (
    init_db,
    get_session
)
from models import (
    BindResponse,
    Profession,
    ProfessionDefault,
    Skill,
    SkillDefault,
    SkillWarriorLink,
    Warrior,
    WarriorDefault,
    WarriorProfessions,
    WarriorSkillsAndProfessions,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)


@app.get("/warriors")
def warrior_list(session=Depends(get_session)) -> List[Warrior]:
    return session.exec(select(Warrior)).all()


@app.get("/warriors/{warrior_id}", response_model=WarriorSkillsAndProfessions)
def warriors_retrieve(warrior_id: int, session=Depends(get_session)) -> Warrior:
    warrior = session.get(Warrior, warrior_id)
    return warrior


@app.post("/warriors")
def warrior_create(warrior: WarriorDefault, session=Depends(get_session)) -> TypedDict('Response', {"status": int,
                                                                                                     "data": Warrior}): # type: ignore
    warrior = Warrior.model_validate(warrior)
    session.add(warrior)
    session.commit()
    session.refresh(warrior)
    return {"status": 200, "data": warrior}


@app.delete("/warriors/{warrior_id}")
def warrior_delete(warrior_id: int, session=Depends(get_session)):
    warrior = session.get(Warrior, warrior_id)
    if not warrior:
        raise HTTPException(status_code=404, detail="Warrior not found")
    session.delete(warrior)
    session.commit()
    return {"ok": True}


@app.patch("/warriors/{warrior_id}")
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


@app.get("/professions")
def professions_list(session=Depends(get_session)) -> List[Profession]:
    return session.exec(select(Profession)).all()


@app.get("/professions/{profession_id}")
def profession_get(profession_id: int, session=Depends(get_session)) -> Profession:
    return session.get(Profession, profession_id)


@app.post("/professions")
def profession_create(prof: ProfessionDefault, session=Depends(get_session)) -> TypedDict('Response', {"status": int,
                                                                                                     "data": Profession}): # type: ignore
    prof = Profession.model_validate(prof)
    session.add(prof)
    session.commit()
    session.refresh(prof)
    return {"status": 200, "data": prof}


@app.get("/skills")
def skill_list(session=Depends(get_session)) -> List[Skill]:
    return session.exec(select(Skill)).all()


@app.get("/skills/{skill_id}")
def skill_get(skill_id: int, session=Depends(get_session)) -> Skill:
    return session.get(Skill, skill_id)


@app.post("/skills")
def skill_create(skill: SkillDefault, session=Depends(get_session)) -> TypedDict('Response', {"status": int,
                                                                                                     "data": Skill}): # type: ignore
    skill = Skill.model_validate(skill)
    session.add(skill)
    session.commit()
    session.refresh(skill)
    return {"status": 200, "data": skill}


@app.post("/bind/{warrior_id}:{skill_id}", response_model=BindResponse)
def bind(warrior_id: int, skill_id: int, session=Depends(get_session)) -> BindResponse:
    warrior = session.get(Warrior, warrior_id)
    skill = session.get(Skill, skill_id)
    
    if not warrior or not skill:
        raise HTTPException(status_code=404, detail="Warrior or Skill not found")
    
    existing_bind = session.exec(
        select(SkillWarriorLink).where(
            SkillWarriorLink.warrior_id == warrior_id,
            SkillWarriorLink.skill_id == skill_id
        )
    ).first()
    
    if existing_bind:
        raise HTTPException(status_code=400, detail="Binding already exists")

    the_bind = SkillWarriorLink(warrior_id=warrior_id, skill_id=skill_id)
    session.add(the_bind)
    session.commit()
    session.refresh(the_bind)
    
    return BindResponse(status=200, data=the_bind)