!!! example "Задание"
    Пошагово реализовать проект и методы, описанные в практике

    Создать API и модели для умений воинов и их ассоциативной сущности, вложено отображать умения при запросе воина

=== "Эндпоинты"

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
    
    
    @app.get("/skills/{skill_id}", response_model=SkillWarrior)
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
    Описание работы -  
    Добавляем зависимости, исключения, импорт базы данных из PgAdmin

![](http://ung1n.github.io/ITMO_ICT_WebDevelopment_tools_2023-2024/img/lab1_and_practics/practic_2_warrior.png)  
    Добавляем в базу данных воина

![](http://ung1n.github.io/ITMO_ICT_WebDevelopment_tools_2023-2024/img/lab1_and_practics/practic_2_skill_list.png)  
    Выводим список скиллов

![](http://ung1n.github.io/ITMO_ICT_WebDevelopment_tools_2023-2024/img/lab1_and_practics/practic_2_skill_id.png)  
    Выводим скилл по id

![](http://ung1n.github.io/ITMO_ICT_WebDevelopment_tools_2023-2024/img/lab1_and_practics/practic_2_skill_create.png)  
    Создаем скилл

![](http://ung1n.github.io/ITMO_ICT_WebDevelopment_tools_2023-2024/img/lab1_and_practics/practic_2_skill_change.png)  
    Изменяем скилл

![](http://ung1n.github.io/ITMO_ICT_WebDevelopment_tools_2023-2024/img/lab1_and_practics/practic_2_skill_delete.png)  
    Удаляем скилл

![](http://ung1n.github.io/ITMO_ICT_WebDevelopment_tools_2023-2024/img/lab1_and_practics/practic_2_skill_link.png)  
    Создаем связь между скиллом и воином

![](http://ung1n.github.io/ITMO_ICT_WebDevelopment_tools_2023-2024/img/lab1_and_practics/practic_2_skilllink_list.png)  
    Выводим список связей между скиллами и воинами

![](http://ung1n.github.io/ITMO_ICT_WebDevelopment_tools_2023-2024/img/lab1_and_practics/practic_2_skilllink_id.png)  
    Выводим связь между скиллом и воином по id скилла и воина


    
=== "Классы"

    ``` py
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
    Описание работы -  
    Добавляем новые классы и ключи между ними

=== "Соединения с базой данных"

    ``` py
    from sqlmodel import SQLModel, Session, create_engine

    db_url = 'postgresql://postgres:1216@localhost/warriors_db'
    engine = create_engine(db_url, echo=True)
    
    
    def init_db():
        SQLModel.metadata.create_all(engine)
    
    
    def get_session():
        with Session(engine) as session:
            yield session
    ```
    Описание работы -  
    Подключаемся к базе данных, создаем таблицы в БД на основе ранее определенных моделей
    функция get_session гарантирует закрытие сессии после использования



