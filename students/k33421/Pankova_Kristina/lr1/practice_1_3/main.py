from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import joinedload
from sqlmodel import select
from starlette.responses import JSONResponse

from db_connection import init_db
from contextlib import asynccontextmanager
from models import *
from db_connection import *
from typing_extensions import TypedDict

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
def hello():
    return "Hello, [username]!"


@app.post("/warrior")
def warriors_create(warrior: WarriorDefault, session=Depends(get_session)) -> TypedDict('Response', {"status": int,
                                                                                                     "data": Warrior}):
    warrior = Warrior.model_validate(warrior)
    session.add(warrior)
    session.commit()
    session.refresh(warrior)
    return {"status": 200, "data": warrior}

@app.get("/warriors_list")
def warriors_list(session=Depends(get_session)) -> List[Warrior]:
    warriors = session.exec(select(Warrior).options(joinedload(Warrior.skills))).unique().all()

    response_data = [
        WarriorResponse(
            id=warrior.id,
            name=warrior.name,
            level=warrior.level,
            skills=[
                SkillResponse(
                    id=skill.id,
                    name=skill.name,
                    description=skill.description
                )
                for skill in warrior.skills
            ]
        )
        for warrior in warriors
    ]
    return JSONResponse(content=[item.dict() for item in response_data])



@app.get("/warriors/{warrior_id}", response_model=WarriorResponse)
def warriors_get(warrior_id: int, session=Depends(get_session)) -> WarriorResponse:
    # Query the database to get the warrior information including the linked skills
    # You can use your ORM of choice (e.g., SQLModel session)
    warrior = session.exec(select(Warrior).where(Warrior.id == warrior_id)).first()
    skills = session.exec(select(Skill).join(SkillWarriorLink).where(SkillWarriorLink.warrior_id == warrior.id)).all()

    # Map the data to the response model
    response_data = WarriorResponse(
        id=warrior.id,
        name=warrior.name,
        level=warrior.level,
        skills=[
            SkillResponse(
                id=skill.id,
                name=skill.name,
                description=skill.description
            )
            for skill in skills
        ]
    )

    return JSONResponse(content=response_data.dict())

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


@app.delete("/warrior/delete{warrior_id}")
def warrior_delete(warrior_id: int, session=Depends(get_session)):
    warrior = session.get(Warrior, warrior_id)
    if not warrior:
        raise HTTPException(status_code=404, detail="Warrior not found")
    session.delete(warrior)
    session.commit()
    return {"ok": True}


@app.post("/skill")
def skills_create(skill: SkillDefault, session=Depends(get_session)) -> TypedDict('Response', {"status": int,
                                                                                                     "data": Skill}):
    skill = Skill.model_validate(skill)
    session.add(skill)
    session.commit()
    session.refresh(skill)
    return {"status": 200, "data": skill}

@app.get("/skills_list")
def skills_list(session=Depends(get_session)) -> List[Skill]:
    return session.exec(select(Skill)).all()


@app.get("/skill/{skill_id}")
def skills_get(skill_id: int, session=Depends(get_session)) -> Skill:
    return session.exec(select(Skill).where(Skill.id == skill_id)).first()


@app.post("/skill_warrior_link")
def skill_warrior_link_create(link: SkillWarriorLink, session=Depends(get_session)):
    link = SkillWarriorLink.model_validate(link)
    session.add(link)
    session.commit()
    session.refresh(link)
    return {"status": 200, "data": link}

@app.get("/skill_warrior_links")
def skill_warrior_links_list(session=Depends(get_session)) -> List[SkillWarriorLink]:
    return session.exec(select(SkillWarriorLink)).all()

@app.get("/skill_warrior_link/{skill_id}/{warrior_id}")
def skill_warrior_link_get(skill_id: int, warrior_id: int, session=Depends(get_session)) -> SkillWarriorLink:
    return session.exec(select(SkillWarriorLink).where((SkillWarriorLink.skill_id == skill_id) & (SkillWarriorLink.warrior_id == warrior_id))).first()

