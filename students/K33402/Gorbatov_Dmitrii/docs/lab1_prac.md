#Практики
Пошагово реализовать проект и методы, описанные в практике.
Создать для временной базы данных модели и API для профессий

##Практика - 1
###Эндпоинты
```py 
from fastapi import FastAPI
from models import Warrior, RaceType, Profession, Skill
from typing_extensions import TypedDict, List

app = FastAPI()

temp_bd = {
    "warriors": [
        {
            "id": 1,
            "race": "director",
            "name": "Мартынов Дмитрий",
            "level": 12,
            "profession": 1,
            "skills": [
                {
                    "id": 1,
                    "name": "Купле-продажа компрессоров",
                    "description": ""
                },
                {
                    "id": 2,
                    "name": "Оценка имущества",
                    "description": ""
                }
            ]
        },
        {
            "id": 2,
            "race": "worker",
            "name": "Андрей Косякин",
            "level": 12,
            "profession": 2,
            "skills": []
        }],

    "professions": [
        {
            "id": 1,
            "title": "Влиятельный человек",
            "description": "Эксперт по всем вопросам"
        },
        {
            "id": 2,
            "title": "Дельфист-гребец",
            "description": "Уважаемый сотрудник"
        }
    ]
}


@app.get("/warriors_list")
def warriors_list() -> List[Warrior]:
    warriors = temp_bd["warriors"]
    return warriors


@app.get("/warrior/{warrior_id}")
def warriors_get(warrior_id: int) -> List[Warrior]:
    warriors = temp_bd["warriors"]
    return [warrior for warrior in warriors if warrior.get("id") == warrior_id]


@app.post("/warrior")
def warriors_create(warrior: Warrior) -> TypedDict('Response', {"status": int, "data": Warrior}):
    warrior_to_append = warrior.model_dump()
    temp_bd["warriors"].append(warrior_to_append)
    return {"status": 200, "data": warrior}


@app.delete("/warrior/delete{warrior_id}")
def warrior_delete(warrior_id: int):
    warriors = temp_bd["warriors"]
    for i, warrior in enumerate(warriors):
        if warrior.get("id") == warrior_id:
            temp_bd["warriors"].pop(i)
            break
    return {"status": 201, "message": "deleted"}


@app.put("/warrior{warrior_id}")
def warrior_update(warrior_id: int, warrior: Warrior) -> List[Warrior]:
    warriors = temp_bd["warriors"]
    for war in warriors:
        if war.get("id") == warrior_id:
            warrior_to_append = warrior.model_dump()
            temp_bd["warriors"].remove(war)
            temp_bd["warriors"].append(warrior_to_append)
    return temp_bd["warriors"]


@app.get("/professions_list")
def professions_list() -> List[Profession]:
    professions = temp_bd["professions"]
    return professions


@app.get("/profession/{profession_id}")
def professions_get(profession_id: int) -> List[Profession]:
    professions = temp_bd["professions"]
    return [profession for profession in professions if profession.get("id") == profession_id]


@app.post("/profession")
def profession_create(profession: Profession) -> TypedDict('Response', {"status": int, "data": Profession}):
    profession_to_append = profession.model_dump()
    temp_bd["professions"].append(profession_to_append)
    return {"status": 200, "data": profession}


@app.put("/profession{profession_id}")
def profession_update(profession_id: int, profession: Profession) -> List[Profession]:
    professions = temp_bd["professions"]
    for prof in professions:
        if prof.get("id") == profession_id:
            profession_to_append = profession.model_dump()
            temp_bd["professions"].remove(prof)
            temp_bd["professions"].append(profession_to_append)
    return temp_bd["professions"]


@app.delete("/profession/delete{profession_id}")
def profession_delete(profession_id: int):
    professions = temp_bd["professions"]
    for i, profession in enumerate(professions):
        if profession.get("id") == profession_id:
            temp_bd["professions"].pop(i)
            break
    return {"status": 201, "message": "deleted"}
```
    
###Описание работы   
Импортируем  FastAPI основной класс для создания приложения, модели и typedict с List temp_bd - словарь который используется как временная база данных и эндпоинты для создания, изменения или просмотра информации о профессиях

![Задание](assets/lab1/a.jpg)  
    Вывожу список профессий

![Задание](assets/lab1/b.jpg)  
    Вывожу профессию по id

![Задание](assets/lab1/c.PNG)  
    Создаю новую профессию

![Задание](assets/lab1/d.PNG)  
    Создаею нового человека

![Задание](assets/lab1/e.PNG)  
    Меняю информацию

![Задание](assets/lab1/f.PNG)  
![Задание](assets/lab1/g.PNG)  
    Удаление 


##Практика - 2
Создать API и модели для умений воинов и их ассоциативной сущности, вложено отображать умения при запросе воина

###Модели

```py
from enum import Enum
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship


class RaceType(Enum):
    director = "director"
    worker = "worker"
    junior = "junior"


class SkillWarriorLink(SQLModel, table=True):
    skill_id: Optional[int] = Field(default=None, foreign_key="skill.id", primary_key=True)
    warrior_id: Optional[int] = Field(default=None, foreign_key="warrior.id", primary_key=True)


class SkillDefault(SQLModel):
    name: str
    description: Optional[str] = ""


class Skill(SkillDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    warriors: Optional[List["Warrior"]] = Relationship(back_populates="skills", link_model=SkillWarriorLink)


class ProfessionDefault(SQLModel):
    title: str
    description: str


class Profession(ProfessionDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    warriors_prof: List["Warrior"] = Relationship(back_populates="profession")


class WarriorDefault(SQLModel):
    race: RaceType
    name: str
    level: int
    profession_id: Optional[int] = Field(default=None, foreign_key="profession.id")


class Warrior(WarriorDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    profession: Optional[Profession] = Relationship(back_populates="warriors_prof")
    skills: Optional[List[Skill]] = Relationship(back_populates="warriors", link_model=SkillWarriorLink)


class WarriorProfessions(WarriorDefault):
    profession: Optional[Profession] = None
    skills: Optional[List[Skill]] = None


class SkillWarrior(SkillDefault):
    warriors: Optional[List[Warrior]] = None
```

###Эндпоинты

``` py
from fastapi import FastAPI, Depends, HTTPException
from typing_extensions import TypedDict, List
from sqlmodel import select

from connection import init_db, get_session
from models import *

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
def warriors_get(warrior_id: int, session=Depends(get_session)) -> WarriorProfessions:
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


@app.get("/skills/{skill_id}", response_model=Skill)
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
```
###Описание работы
Добавляем зависимости, исключения, импорт базы данных из PgAdmin

![](assets/lab1/h.PNG)  
Создаю профессию

![](assets/lab1/i.PNG)  
Создаю скилл

![](assets/lab1/j.PNG)  
При запросе война скилл отображается вложенно

##Практика - 3
###.env
```py 
DB_ADMIN = postgresql://postgres:123@localhost/warriors_db
```
###alembic.ini
Как я передал URL базы в alembic.ini с помощью .env 

```py
sqlalchemy.url = os.getenv('DB_ADMIN')
```

###connections.py
Как происходит соединение с БД
```py
from sqlmodel import SQLModel, Session, create_engine

import os
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv('DB_ADMIN')
engine = create_engine(db_url, echo=True)
```


##Вывод
В ходе выполнения практического задания я успешно реализовал все улучшения, описанные в практике, что позволило повысить качество кода. 
А также разобрался с работой FastAPI.