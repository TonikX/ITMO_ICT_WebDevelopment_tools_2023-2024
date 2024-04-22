#Практика 3 Миграции, ENV, GitIgnore и структура проекта

models.py

    from enum import Enum
    from typing import List, Optional
    
    # from pydantic import BaseModel
    from sqlmodel import Field, Relationship, SQLModel
    
    
    class RaceType(Enum):
        director = "director"
        worker = "worker"
        junior = "junior"
    
    
    class SkillWarriorLink(SQLModel, table=True):
        skill_id: Optional[int] = Field(default=None, foreign_key="skill.id", primary_key=True)
        warrior_id: Optional[int] = Field(default=None, foreign_key="warrior.id", primary_key=True)
        level: int | None
    
    
    class Skill(SQLModel, table=True):
        id: int = Field(default=None, primary_key=True)
        name: str
        description: Optional[str] = ""
        warriors: Optional[List["Warrior"]] = Relationship(back_populates="skills", link_model=SkillWarriorLink)
    
    
    class Profession(SQLModel, table=True):
        id: int = Field(default=None, primary_key=True)
        title: str
        description: str
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

connection.py

    import os
    
    from dotenv import load_dotenv
    from sqlmodel import Session, SQLModel, create_engine
    
    load_dotenv()
    
    engine = create_engine(os.getenv("DB_ADMIN"), echo=True)
    
    
    def init_db():
        SQLModel.metadata.create_all(engine)
    
    
    def get_session():
        with Session(engine) as session:
            yield session

main.py

    from http import HTTPStatus
    
    from fastapi import Depends, FastAPI, HTTPException
    from sqlmodel import Session, select
    from typing_extensions import TypedDict
    
    from connection import get_session, init_db
    from models import *
    
    app = FastAPI()
    
    
    class MessageResponse(TypedDict):
        message: str
    
    
    @app.on_event("startup")
    def on_startup():
        init_db()
    
    
    @app.get("/warriors")
    def warriors_list(session: Session = Depends(get_session)) -> list[Warrior]:
        return session.exec(select(Warrior)).all()
    
    
    @app.get("/warriors/{warrior_id}", response_model=WarriorProfessions)
    def warriors_get(warrior_id: int, session: Session = Depends(get_session)) -> list[Warrior]:
        return session.exec(select(Warrior).where(Warrior.id == warrior_id)).first()
    
    
    @app.post("/warriors")
    def warriors_create(warrior: Warrior, session: Session = Depends(get_session)) -> Warrior:
        warrior = Warrior.model_validate(warrior)
        session.add(warrior)
        session.commit()
        session.refresh(warrior)
        return warrior
    
    
    @app.delete("/warriors/{warrior_id}")
    def warrior_delete(warrior_id: int, session: Session = Depends(get_session)) -> MessageResponse:
        session.delete(session.get(Warrior, warrior_id))
        session.commit()
        return {"message": "deleted"}
    
    
    @app.put("/warriors/{warrior_id}")
    def warrior_update(warrior_id: int, warrior: Warrior, session: Session = Depends(get_session)) -> Warrior:
        db_warrior = session.get(Warrior, warrior_id)
        if not db_warrior:
            raise HTTPException(status_code=404, detail="Warrior not found")
        warrior_data = warrior.model_dump(exclude_unset=True)
        db_warrior.sqlmodel_update(warrior_data)
        session.add(db_warrior)
        session.commit()
        session.refresh(db_warrior)
        return db_warrior
    
    
    @app.post("/warriors/{warrior_id}/skills/{skill_id}", response_model=WarriorProfessions)
    def warrior_append_skill(warrior_id: int, skill_id: int, session: Session = Depends(get_session)) -> Warrior:
        if (skill := session.exec(select(Skill).where(Skill.id == skill_id)).first()) is None:
            raise HTTPException(HTTPStatus.NOT_FOUND, {"message": "skill was not found"})
        if (warrior := session.exec(select(Warrior).where(Warrior.id == warrior_id)).first()) is None:
            raise HTTPException(HTTPStatus.NOT_FOUND, {"message": "warrior was not found"})
        warrior.skills.append(skill)
        session.add(warrior)
        session.commit()
        session.refresh(warrior)
        return warrior
    
    
    @app.delete("/warriors/{warrior_id}/skills/{skill_id}", response_model=WarriorProfessions)
    def warrior_delete_skill(warrior_id: int, skill_id: int, session: Session = Depends(get_session)) -> Warrior:
        if (warrior := session.exec(select(Warrior).where(Warrior.id == warrior_id)).first()) is None:
            raise HTTPException(HTTPStatus.NOT_FOUND, {"message": "warrior was not found"})
        if (skill_idx := next((i for i, j in enumerate(warrior.skills) if j.id == skill_id), None)) is None:
            raise HTTPException(HTTPStatus.NOT_FOUND, {"message": "skill was not found"})
        warrior.skills.pop(skill_idx)
        session.add(warrior)
        session.commit()
        session.refresh(warrior)
        return warrior
    
    
    @app.get("/professions")
    def get_professions(session: Session = Depends(get_session)) -> list[Profession]:
        return session.exec(select(Profession)).all()
    
    
    @app.get("/professions/{profession_id}")
    def get_profession(profession_id: int, session: Session = Depends(get_session)) -> Profession:
        return session.exec(select(Profession).where(Profession.id == profession_id)).first()
    
    
    @app.post("/professions")
    def create_profession(profession: Profession, session: Session = Depends(get_session)) -> Profession:
        profession = Profession.model_validate(profession)
        session.add(profession)
        session.commit()
        session.refresh(profession)
        return profession
    
    
    @app.put("/professions/{profession_id}")
    def update_profession(
        profession_id: int, profession: Profession, session: Session = Depends(get_session)
    ) -> Profession:
        db_profession = session.get(Profession, profession_id)
        if not db_profession:
            raise HTTPException(status_code=404, detail="profession not found")
        profession_data = profession.model_dump(exclude_unset=True)
        db_profession.sqlmodel_update(profession_data)
        session.add(db_profession)
        session.commit()
        session.refresh(db_profession)
        return db_profession
    
    
    @app.delete("/professions/{profession_id}")
    def delete_profession(profession_id: int, session: Session = Depends(get_session)) -> MessageResponse:
        session.delete(session.get(Profession, profession_id))
        session.commit()
        return {"message": "deleted"}
    
    
    @app.get("/skills")
    def get_skills(session: Session = Depends(get_session)) -> list[Skill]:
        return session.exec(select(Skill)).all()
    
    
    @app.get("/skills/{skill_id}")
    def get_skill(skill_id: int, session: Session = Depends(get_session)) -> Skill:
        return session.exec(select(Skill).where(Skill.id == skill_id)).first()
    
    
    @app.post("/skills")
    def create_skill(skill: Skill, session: Session = Depends(get_session)) -> Skill:
        skill = Skill.model_validate(skill)
        session.add(skill)
        session.commit()
        session.refresh(skill)
        return skill
    
    
    @app.put("/skills/{skill_id}")
    def update_skill(skill_id: int, skill: Skill, session: Session = Depends(get_session)) -> Skill:
        db_skill = session.get(Skill, skill_id)
        if not db_skill:
            raise HTTPException(status_code=404, detail="Skill not found")
        db_skill.sqlmodel_update(skill)
        session.add(db_skill)
        session.commit()
        session.refresh(db_skill)
        return db_skill
    
    
    @app.delete("/skills/{skill_id}")
    def delete_skill(skill_id: int, session: Session = Depends(get_session)) -> MessageResponse:
        session.delete(session.get(Skill, skill_id))
        session.commit()
        return {"message": "Skill deleted"}

Evn.py из моего проекта 

    from logging.config import fileConfig
    
    from sqlalchemy import engine_from_config
    from sqlalchemy import pool
    
    from alembic import context
    
    from travel_app.models import *
    # this is the Alembic Config object, which provides
    # access to the values within the .ini file in use.
    config = context.config
    
    # Interpret the config file for Python logging.
    # This line sets up loggers basically.
    if config.config_file_name is not None:
        fileConfig(config.config_file_name)
    
    # add your model's MetaData object here
    # for 'autogenerate' support
    # from myapp import mymodel
    # target_metadata = mymodel.Base.metadata
    target_metadata = Base.metadata
    
    # other values from the config, defined by the needs of env.py,
    # can be acquired:
    # my_important_option = config.get_main_option("my_important_option")
    # ... etc.
    
    
    def run_migrations_offline() -> None:
        """Run migrations in 'offline' mode.
    
        This configures the context with just a URL
        and not an Engine, though an Engine is acceptable
        here as well.  By skipping the Engine creation
        we don't even need a DBAPI to be available.
    
        Calls to context.execute() here emit the given string to the
        script output.
    
        """
        url = config.get_main_option("sqlalchemy.url")
        context.configure(
            url=url,
            target_metadata=target_metadata,
            literal_binds=True,
            dialect_opts={"paramstyle": "named"},
        )
    
        with context.begin_transaction():
            context.run_migrations()
    
    
    def run_migrations_online() -> None:
        """Run migrations in 'online' mode.
    
        In this scenario we need to create an Engine
        and associate a connection with the context.
    
        """
        connectable = engine_from_config(
            config.get_section(config.config_ini_section, {}),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
        )
    
        with connectable.connect() as connection:
            context.configure(
                connection=connection, target_metadata=target_metadata
            )
    
            with context.begin_transaction():
                context.run_migrations()
    
    
    if context.is_offline_mode():
        run_migrations_offline()
    else:
        run_migrations_online()
