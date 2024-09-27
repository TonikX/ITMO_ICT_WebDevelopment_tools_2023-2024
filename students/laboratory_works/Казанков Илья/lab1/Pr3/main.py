from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from Lr1.auth import verify_password, get_password_hash
from models import Task, TaskBase, TaskShow, User, UserBase, ChangePassword
from database import init_db, get_session
from typing_extensions import TypedDict

app = FastAPI()


@app.on_event("startup")
def on_startup():
    init_db()


# Создание задачи
@app.post("/task-create")
def task_create(task: TaskBase, session=Depends(get_session)) -> TypedDict('Response', {"status": int, "data": Task}):
    task = Task(**task.dict())
    session.add(task)
    session.commit()
    session.refresh(task)
    return {"status": 200, "data": task}


@app.get("/list-tasks")
def tasks_list(session=Depends(get_session)) -> list[Task]:
    return session.query(Task).all()


@app.get("/task/{task_id}", response_model=TaskShow)
def task_get(task_id: int, session=Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.patch("/task/update/{task_id}")
def task_update(task_id: int, task: TaskBase, session=Depends(get_session)) -> Task:
    db_task = session.get(Task, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    task_data = task.dict(exclude_unset=True)
    for key, value in task_data.items():
        setattr(db_task, key, value)

    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


@app.delete("/task/delete/{task_id}")
def task_delete(task_id: int, session=Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    session.delete(task)
    session.commit()
    return {"ok": True}


@app.post("/user-create")
def user_create(user: UserBase, session=Depends(get_session)) -> TypedDict('Response', {"status": int, "data": User}):
    user = User(**user.dict())
    session.add(user)
    session.commit()
    session.refresh(user)
    return {"status": 200, "data": user}


@app.get("/list-users")
def users_list(session=Depends(get_session)) -> list[User]:
    return session.query(User).all()


@app.get("/user/{user_id}", response_model=UserBase)
def user_get(user_id: int, session=Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.patch("/user/update/{user_id}")
def user_update(user_id: int, user: UserBase, session=Depends(get_session)) -> User:
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    user_data = user.dict(exclude_unset=True)
    for key, value in user_data.items():
        setattr(db_user, key, value)

    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@app.delete("/user/delete/{user_id}")
def user_delete(user_id: int, session=Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    session.delete(user)
    session.commit()
    return {"ok": True}


@app.patch("/user/change-password/{user_id}")
def change_password(user_id: int, password_data: ChangePassword, session=Depends(get_session)) -> TypedDict('Response',
                                                                                                            {
                                                                                                                "status": int,
                                                                                                                "message": str}):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(password_data.old_password, user.password):
        raise HTTPException(status_code=400, detail="Invalid old password")

    user.password = get_password_hash(password_data.new_password)

    session.add(user)
    session.commit()
    session.refresh(user)
    return {"status": 200, "message": "Password changed successfully"}
