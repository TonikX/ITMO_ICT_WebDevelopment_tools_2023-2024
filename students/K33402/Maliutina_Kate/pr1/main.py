from typing import TypedDict

from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import select

from db import *
from models import *

app = FastAPI()  # создаем приложение


@app.on_event("startup")  # при событии запуска выполняется эта функция
def on_startup():
    init_db()  # вызов функции из файла db.py


@app.get("/")  # при гет запросе на главной странице вызывается эта функция
def hello():
    return "Hello, [username]!"


@app.get("/warriors")
def warriors(session=Depends(get_session)) -> List[Warrior]:  # в параметры передаем сессию для выполнения запросов в БД
    # после -> идет возвращаемый тип, тут возвращается список войнов
    return session.exec(select(Warrior)).all()  # внутри сессии выполняется запрос select, выбирая всех войнов


@app.get("/warrior/{warrior_id}", response_model=WarriorProfessions)  # выполняется гет метод по пути, типа /warrior/1, где 1 - id война
def warriors_get(warrior_id: int, session=Depends(get_session)) -> Warrior:
    warrior = session.get(Warrior, warrior_id)  # внутри сессии выполняется гет запрос (select) с фильтром по полю id
    return warrior


@app.post("/warrior")  # при пост запросе выполняется запрос на создание модели
def warriors_create(warrior: WarriorDefault, session=Depends(get_session)) -> (
        TypedDict('Response', {"status": int, "data": Warrior})):
    # из этой функции возвращается словарь, где хранится ответ (Response) типа JSON, внутри которого есть статус и воин
    war = Warrior.model_validate(warrior)  # валидируем переданного война
    session.add(war)  # создаем война
    session.commit()  # подтверждаем изменения
    session.refresh(war)  # обновляем модель с дефолтными значениями
    return {"status": 200, "data": war}


@app.delete("/warrior/delete{warrior_id}")  # при делит запросе удаляется запись с переданным id
def warrior_delete(warrior_id: int, session=Depends(get_session)):
    war = session.get(Warrior, warrior_id)  # получаем модель из БД
    if not war:  # если воина такого нет, то возвращаем исключение
        raise HTTPException(status_code=404, detail="Warrior not found")
    session.delete(war)  # удаляем воина
    session.commit()  # подтверждаем изменения
    return {"ok": True}


@app.patch("/warrior{warrior_id}")  # при выполнении патч запроса модель обновляется с переданным id
def warrior_update(warrior_id: int, warrior: WarriorDefault, session=Depends(get_session)) -> WarriorDefault:
    db_warrior = session.get(Warrior, warrior_id)  # получаем модель из БД
    if not db_warrior:  # если воина такого нет, то возвращаем исключение
        raise HTTPException(status_code=404, detail="Warrior not found")
    warrior_data = warrior.model_dump(exclude_unset=True)  # полученная модель в параметрах преобразуется в json с получением только измененных полей (флаг exclude_unset)
    for key, value in warrior_data.items():  # проходимся в цикле по всем полям
        setattr(db_warrior, key, value)  # обновляем все указанные поля
    session.add(db_warrior)  # устанавливаем воина
    session.commit()  # подтверждаем изменения
    session.refresh(db_warrior)  # обновляем модель
    return db_warrior


@app.get("/professions")  # получение всех профессий
def professions(session=Depends(get_session)) -> List[Profession]:
    return session.exec(select(Profession)).all()


@app.get("/profession/{profession_id}")
def profession_get(profession_id: int, session=Depends(get_session)) -> Profession:
    return session.get(Profession, profession_id)


@app.post("/profession")
def profession_create(prof: Profession, session=Depends(get_session)) -> (
        TypedDict('Response', {"status": int, "data": Profession})):
    prof = Profession.model_validate(prof)
    session.add(prof)
    session.commit()
    session.refresh(prof)
    return {"status": 200, "data": prof}
