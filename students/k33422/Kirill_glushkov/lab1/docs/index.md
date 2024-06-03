# Документация 1

**Задание:** Разработка сервиса для управления личными финансами
Необходиом создать простой сервис для управления личными финансами. Сервис должен позволять пользователям вводить доходы и расходы, устанавливать бюджеты на различные категории, а также просматривать отчеты о своих финансах. Дополнительные функции могут включать в себя возможность получения уведомлений о превышении бюджета, анализа трат и установки целей на будущее.

**Практика:1**

# Практическое задание

## Реализация по модели из практического задания

### Шаги реализации

1. Пошагово реализовать проект и методы, описанные в практике
2. Создать для временной базы данных модели и API для профессий

## Реализация по модели из своего варианта

### Шаги реализации

1. Сделать временную базу для главной таблицы (2-3 записи), по аналогии с практикой (должны иметь одиночный вложенный объект и список объектов)
2. Выполнить действия описанные в практике для своего проекта
3. Сделать модели и API для вложенного объекта

## Код реализации

### main.py
```python
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy.orm import Session
import uvicorn
from datetime import datetime
from app.database import SessionLocal
from app.models import Budget, Expense, Income, User
from sqlalchemy import and_, func

temp_bd = [
    User(id=1, name="Мартынов Дмитрий", incomes=[Income(date='2024-05-28', amount=1000.0, category='salary'), Income(date='2024-06-01', amount=500.0, category='bonus')], 
         expenses=[Expense(date='2024-05-28', amount=500.0, category='rent'), Expense(date='2024-06-01', amount=200.0, category='food')], 
         budgets=[Budget(category='rent', amount=1000.0), Budget(category='food', amount=500.0)]),
    User(id=2, name="Петров Иван", incomes=[Income(date='2024-05-29', amount=800.0, category='salary'), Income(date='2024-06-02', amount=300.0, category='bonus')], 
         expenses=[Expense(date='2024-05-29', amount=300.0, category='rent'), Expense(date='2024-06-02', amount=150.0, category='food')], 
         budgets=[Budget(category='rent', amount=800.0), Budget(category='food', amount=300.0)]),
    User(id=3, name="Сидоров Сергей", incomes=[Income(date='2024-05-30', amount=1200.0, category='salary'), Income(date='2024-06-03', amount=400.0, category='bonus')], 
         expenses=[Expense(date='2024-05-30', amount=400.0, category='rent'), Expense(date='2024-06-03', amount=200.0, category='food')], 
         budgets=[Budget(category='rent', amount=1200.0), Budget(category='food', amount=400.0)]),
]

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

@app.on_event("startup")
def startup():
    with SessionLocal() as session:
        session.execute("SELECT 1")

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/temp_db")
async def get_temp_db():
    return temp_bd

@app.delete("/temp_db/{user_id}")
async def delete_user(user_id: int):
    for user in temp_bd:
        if user["id"] == user_id:
            temp_bd.remove(user)
            return {"message": "User deleted"}
    raise HTTPException(status_code=404, detail="User not found")

@app.put("/temp_db/{user_id}")
async def update_user(user_id: int, user: User):
    for user_db in temp_bd:
        if user_db["id"] == user_id:
            user_db["name"] = user.name
            user_db["incomes"] = user.incomes
            user_db["expenses"] = user.expenses
            user_db["budgets"] = user.budgets
            return {"id": user_id, "name": user.name, "incomes": user.incomes, "expenses": user.expenses, "budgets": user.budgets}
    raise HTTPException(status_code=404, detail="User not found")

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True, workers=1, log_level='debug', access_log=True)
```

**Практика:2**

# Практическое задание

## Реализация по модели из практического задания

### Шаги реализации

1. Пошагово реализовать проект и методы, описанные в практике
2. Создать API и модели для умений воинов и их ассоциативной сущности, вложено отображать умения при запросе воина

## Реализация по модели из своего варианта

### Шаги реализации

1. Пошагово реализовать подключение к БД, АПИ и модели, на основании своего варианта основываясь на действиях в практике
2. Сделать модели и API для many-to-many связей с вложенным отображением

## Код реализации

### main.py
```python
from typing import List
from fastapi import APIRouter, FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
import uvicorn
from datetime import datetime, timedelta
from app.database import SessionLocal,  init_db, BudgetDB, ExpenseDB, UserDB, IncomeDB
from app.models import Income, Expense, Budget, User
from bcrypt import hashpw, gensalt
import jwt

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI(swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"})
router = APIRouter()

class Token(BaseModel):
    access_token: str
    token_type: str

def generate_token(username: str) -> str:
    expiration = datetime.now() + timedelta(minutes=30)
    token_data = {
        "sub": username,
        "exp": expiration
    }
    token = jwt.encode(token_data, "secret", algorithm="HS256")
    return token

@app.on_event("startup")
def startup():
    init_db()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@router.get("/users")
async def get_users() -> List[User]:
    with SessionLocal() as db:
        users = db.query(UserDB).all()
        return users

@router.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int):
    with SessionLocal() as db:
        user = db.query(UserDB).filter(UserDB.id == user_id).first()
        print(user, 'usr')
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user

@router.delete("/users/{user_id}")
async def delete_user(user_id: int):
    with SessionLocal() as db:
        db_user = db.query(UserDB).get(user_id)
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        db.delete(db_user)
        db.commit()
        return JSONResponse(status_code=204, content="User deleted")

@router.post("/users", response_model=User)
async def create_user(user: User):
    with SessionLocal() as db:
        salt = gensalt()
        user_data = user.model_dump(exclude={'password'})
        db_user = UserDB(**user_data, password=str(hashpw(user.password.encode(), salt)))
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

def verify_pwd(password: str, hashed_password: str) -> bool:
    salt = gensalt()
    return str(hashpw(password.encode(), salt)) == hashed_password

@router.post("/users/login")
async def login(user: User):
    with SessionLocal() as db:
        db_user = db.query(UserDB).filter(UserDB.username == user.username).first()
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        if not verify_pwd(user.password, db_user.password):
            raise HTTPException(status_code=401, detail="Invalid password")
        token = generate_token(db_user.username)
        return {"access_token": token, "token_type": "bearer"}

@router.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, user: User):
    with SessionLocal() as db:
        db_user = db.query(UserDB).filter(UserDB.id == user_id).first()
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        for var, value in vars(user).items():
            setattr(db_user, var, value)
        db.commit()
        db.refresh(db_user)
        return db_user

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True, workers=1, log_level='debug', access_log=True)
```
# Практическое задание

## Реализация по модели из практического задания

### Шаги реализации

1. Пошагово реализовать проект и методы, описанные в практике
2. Создать API и модели для умений воинов и их ассоциативной сущности, вложено отображать умения при запросе воина

## Реализация по модели из своего варианта

### Шаги реализации

1. Реализовать в своем проекте все улучшения, описанные в практике
2. Разобраться как передать в alembic.ini URL базы данных с помощью.env-файла и реализовать подобную передачу.

## Код реализации

### /pr3
### connection.py

```python
import os

from dotenv import load_dotenv
from sqlmodel import SQLModel, Session, create_engine

load_dotenv()
db_url = os.getenv('DB_ADMIN')
engine = create_engine(db_url, echo=True)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
```
### main.py

```python
from enum import Enum
from typing import Optional, List

# from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Relationship


class RaceType(Enum):
    director = "director"
    worker = "worker"
    junior = "junior"


class SkillWarriorLink(SQLModel, table=True):
    skill_id: Optional[int] = Field(
        default=None, foreign_key="skill.id", primary_key=True
    )
    warrior_id: Optional[int] = Field(
        default=None, foreign_key="warrior.id", primary_key=True
    )
    level: int | None


class SkillDefault(SQLModel):
    name: str
    description: str


class Skill(SkillDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    warriors: Optional[List["Warrior"]] = Relationship(back_populates="skills", link_model=SkillWarriorLink,
                                                       sa_relationship_kwargs={
                                                           "cascade": "all, delete",
                                                       })


class ProfessionDefault(SQLModel):
    title: str
    description: str


class Profession(ProfessionDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    warriors_prof: List["Warrior"] = Relationship(back_populates="profession", sa_relationship_kwargs={
        "cascade": "all, delete"})


class WarriorDefault(SQLModel):
    race: RaceType
    name: str
    level: int
    profession_id: Optional[int] = Field(default=None, foreign_key="profession.id")


class Warrior(WarriorDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    profession: Optional[Profession] = Relationship(back_populates="warriors_prof", sa_relationship_kwargs={
        "cascade": "all, delete"})
    skills: Optional[List[Skill]] = Relationship(back_populates="warriors", link_model=SkillWarriorLink,
                                                 sa_relationship_kwargs={
                                                     "cascade": "all, delete"})


class WarriorProfessions(WarriorDefault):
    profession: Optional[Profession] = None


class WarriorSkills(WarriorDefault):
    skill: Optional[Skill] = None
```

### models.py

```python
from enum import Enum
from typing import Optional, List

#from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Relationship


class RaceType(Enum):
    director = "director"
    worker = "worker"
    junior = "junior"


class SkillWarriorLink(SQLModel, table=True):
    skill_id: Optional[int] = Field(
        default=None, foreign_key="skill.id", primary_key=True
    )
    warrior_id: Optional[int] = Field(
        default=None, foreign_key="warrior.id", primary_key=True
    )


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


class Warrior(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    race: RaceType
    name: str
    level: int
    profession_id: Optional[int] = Field(default=None, foreign_key="profession.id")
    profession: Optional[Profession] = Relationship(back_populates="warriors_prof")
    skills: Optional[List[Skill]] = Relationship(back_populates="warriors", link_model=SkillWarriorLink)
```