from fastapi import FastAPI, Depends, HTTPException
from db import get_session, init_db
from sqlmodel import select, Session
from typing import TypedDict
from models import *

app = FastAPI()


@app.get("/")
def hello():
    return "Hello, [username]!"


@app.on_event('startup')
def on_startup():
    init_db()


@app.get('/warrior/list')
def get_warrior_list(session=Depends(get_session)) -> List[Warrior]:
    return session.exec(select(Warrior)).all()


@app.get('/warrior/{warrior_id}')
def get_warrior_by_id(
        warrior_id:int,
        session:Session=Depends(get_session)
) -> Warrior:
    warrior = session.get(Warrior, warrior_id)
    if warrior is None:
        raise HTTPException(
            status_code=404,
            detail=f'no warrior with id: {warrior_id}'
        )
    return warrior # то, что он ругается на Type[Warrior] или WarriorProfessions - это фигня


@app.post('/warrior/create')
def create_warrior(warrior: BaseWarrior, session=Depends(get_session)) -> Warrior:
    warrior = Warrior.model_validate(warrior)
    session.add(warrior)
    session.commit()
    session.refresh(warrior)
    return warrior





@app.patch('/warrior/patch/{warrior_id}')
def patch_warrior(
        warrior_id: int,
        warrior: WarriorUpdate,
        session:Session=Depends(get_session)
) -> TypedDict('response', {'status_code': int, 'data': Warrior}):
    # Получаем воина для обнавления
    db_warrior = session.get(Warrior, warrior_id)
    if not db_warrior:
        raise HTTPException(status_code=404, detail="Warrior not found")
    # Получаем словарь
    warrior_data = warrior.model_dump(exclude_unset=True)
    # Обновляем
    db_warrior.sqlmodel_update(warrior_data)
    # Обычные действия с БД
    session.add(db_warrior)
    session.commit()
    session.refresh(db_warrior)
    # status_code ни на что не влияет. Это просто поле в ответе
    return {'status_code': 200, 'data': db_warrior}


@app.get("/professions_list")
def professions_list(session=Depends(get_session)) -> List[Profession]:
    return session.exec(select(Profession)).all()


@app.get("/profession/{profession_id}")
def profession_get(profession_id: int, session=Depends(get_session)) -> Profession:
    return session.get(Profession, profession_id)


@app.post("/profession")
def profession_create(prof: BaseProfession, session=Depends(get_session)) -> TypedDict('Response', {"status": int,
                                                                                                     "data": Profession}):
    prof = Profession.model_validate(prof)
    session.add(prof)
    session.commit()
    session.refresh(prof)
    return {"status": 200, "data": prof}
