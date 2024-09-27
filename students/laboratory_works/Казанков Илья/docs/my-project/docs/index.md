# Лабораторная раб. 1

Научиться реализовывать полноценное серверное приложение с помощью фреймворка FastAPI с применением дополнительных средств и библиотек. 
Задача состоит в разработке программной системы, которая будет использоваться для тайм-менеджера

Разработайте простую программу-тайм-менеджер, которая поможет управлять вашим временем и задачами. Программа должна позволять создавать задачи с описанием, устанавливать им сроки выполнения и приоритеты, а также отслеживать затраченное время на каждую задачу.
## Ход выполнения работы

### main.py
```
from fastapi import FastAPI
import uvicorn
from database import init_db
from auth_endpoints import auth_router
from user_endpoints import user_router
from task_endpoints import task_router

app = FastAPI()

app.include_router(auth_router, prefix="/api", tags=["auth"])
app.include_router(user_router, prefix="/api/users", tags=["users"])
app.include_router(task_router, prefix="/api/tasks", tags=["tasks"])

@app.on_event("startup")
def on_startup():
    init_db()

if __name__ == '__main__':
    uvicorn.run('main:app', host="localhost", port=8000, reload=True)

```

### database.py
```
from sqlmodel import SQLModel, Session, create_engine
import os
from dotenv import load_dotenv

load_dotenv()
a=os.getenv('DB_URL')
print(a)
engine = create_engine(os.getenv('DB_URL'), echo=True)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
```

### task_endpoints.py
```
from fastapi import APIRouter
from models import Task, TaskBase, TaskShow, User
from typing_extensions import TypedDict
import datetime
from fastapi import HTTPException, Depends
from database import get_session

task_router = APIRouter()

@task_router.post("/tasks/create")
def task_create(task: TaskBase, user_id: int, session=Depends(get_session)) -> TypedDict('Response', {"status": int, "data": Task}):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    task = Task.model_validate(task)
    task.user_id = user_id
    session.add(task)
    session.commit()
    session.refresh(task)
    return {"status": 200, "data": task}

@task_router.get("/tasks/list")
def task_list(session=Depends(get_session)) -> list[Task]:
    return session.query(Task).all()

@task_router.get("/tasks/{task_id}", response_model=TaskShow)
def task_get(task_id: int, session=Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@task_router.patch("/tasks/update/{task_id}")
def task_update(task_id: int, task: TaskBase, session=Depends(get_session)) -> Task:
    db_task = session.get(Task, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    task_data = task.model_dump(exclude_unset=True)
    for key, value in task_data.items():
        setattr(db_task, key, value)

    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

@task_router.delete("/tasks/delete/{task_id}")
def task_delete(task_id: int, session=Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    session.delete(task)
    session.commit()
    return {"ok": True}

@task_router.patch("/tasks/time-spent/{task_id}")
def update_time_spent(task_id: int, time_spent: int, session=Depends(get_session)) -> Task:
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.time_spent += time_spent

    if datetime.datetime.now() >= task.date_end and not task.status:
        task.status = True

    session.add(task)
    session.commit()
    session.refresh(task)
    return task
```
### auth_endpoints.py
```
from fastapi import APIRouter
from auth import *
from database import get_session
from models import UserBase, User, UserShow, ChangePassword
from sqlmodel import select


auth_router = APIRouter()


@auth_router.post('/registration', status_code=201, description='Register new user')
def register(user: UserBase, session=Depends(get_session)):
    users = session.exec(select(User)).all()
    if any(x.username == user.username for x in users):
        raise HTTPException(status_code=400, detail='Username is taken')
    hashed_pwd = get_password_hash(user.password)
    user = User(username=user.username, password=hashed_pwd)
    session.add(user)
    session.commit()
    return {"status": 201, "message": "Created"}


@auth_router.post('/login')
def login(user: UserBase, session=Depends(get_session)):
    user_found = session.exec(select(User).where(User.username == user.username)).first()
    if not user_found:
        raise HTTPException(status_code=401, detail='Invalid username and/or password')
    verified = verify_password(user.password, user_found.password)
    if not verified:
        raise HTTPException(status_code=401, detail='Invalid username and/or password')
    token = encode_token(user_found.username)
    return {'token': token}


@auth_router.get('/me', response_model=UserShow)
def get_current_user(user: User = Depends(get_current_user)) -> User:
    return user


@auth_router.patch("/me/change-password")
def user_pwd(user_pwd: ChangePassword, session=Depends(get_session), current=Depends(get_current_user)):
    found_user = session.get(User, current.id)
    if not found_user:
        raise HTTPException(status_code=404, detail="User not found")
    verified = verify_password(user_pwd.old_password, found_user.password)
    if not verified:
        raise HTTPException(status_code=400, detail="Invalid old password")
    hashed_pwd = get_password_hash(user_pwd.new_password)
    found_user.password = hashed_pwd
    session.add(found_user)
    session.commit()
    session.refresh(found_user)
    return {"status": 200, "message": "password changed successfully"}
```
### user_endpoints.py
```
from fastapi impofrom fastapi import APIRouter, HTTPException
from fastapi import Depends
from models import UserBase, User, UserShow
from database import get_session
from sqlmodel import select

user_router = APIRouter()

@user_router.get("/users/list")
def user_list(session=Depends(get_session)) -> list[User]:
    users = session.exec(select(User)).all()
    user_models = [user.model_dump(exclude={'password'}) for user in users]
    return user_models

@user_router.get("/users/{user_id}", response_model=UserShow)
def user_get(user_id: int, session=Depends(get_session)) -> UserShow:
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@user_router.delete("/users/delete/{user_id}")
def user_delete(user_id: int, session=Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return {"ok": True}
```
### models.py
```
from sqlmodel import SQLModel, Field, Relationship
from enum import Enum
from typing import Optional, List
import datetime

class TaskPriority(Enum):
    low = "low"
    medium = "medium"
    high = "high"

class TaskBase(SQLModel):
    title: str
    description: str
    date_start: datetime.date
    date_end: datetime.date
    priority: TaskPriority = TaskPriority.medium
    time_spent: Optional[int] = 0

class TaskShow(TaskBase):
    status: Optional[bool] = False

class Task(TaskBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    status: Optional[bool] = False
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    user: list['User'] = Relationship(back_populates="tasks")

class UserBase(SQLModel):
    username: str
    password: str

class UserShow(UserBase):
    tasks: Optional[List["Task"]] = None

class User(UserBase, table=True):
    id: int = Field(default=None, primary_key=True)
    tasks: Optional[List["Task"]] = Relationship(back_populates="user")

class ChangePassword(SQLModel):
    old_password: str
    new_password: str
```
### auth.py
```
import datetime
from fastapi import Security, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
import jwt
from starlette import status
from database import get_session
from models import User
from sqlmodel import select

# Global environment variables
security = HTTPBearer()
pwd_context = CryptContext(schemes=['bcrypt'])
secret_key = 'supersecret'


def get_password_hash(password):
    print(pwd_context.hash(password))
    return pwd_context.hash(password)


def verify_password(password, hashed_password):
    return pwd_context.verify(password, hashed_password)


def encode_token(user_id):
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=8),
        'iat': datetime.datetime.utcnow(),
        'sub': user_id
    }
    return jwt.encode(payload, secret_key, algorithm='HS256')


def decode_token(token):
    try:
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        return payload['sub']
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail='Expired signature')
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail='Invalid token')


def auth_wrapper(auth: HTTPAuthorizationCredentials = Security(security)):
    return decode_token(auth.credentials)


def get_current_user(auth: HTTPAuthorizationCredentials = Security(security), session=Depends(get_session)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials'
    )
    username = decode_token(auth.credentials)
    if username is None:
        raise credentials_exception
    user = session.exec(select(User).where(User.username == username)).first()
    if user is None:
        raise credentials_exception
    return user
```
