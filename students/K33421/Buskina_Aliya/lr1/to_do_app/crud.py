from datetime import date

from sqlalchemy.orm import Session
import models

def create_user(db: Session, username: str, hashed_password: str, is_active: bool = True):
    db_user = models.User(username=username, hashed_password=hashed_password, is_active=is_active)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def update_user(db: Session, user_id: int, username: str, hashed_password: str, is_active: bool = True):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db_user.username = username
        db_user.hashed_password = hashed_password
        db_user.is_active = is_active
        db.commit()
        db.refresh(db_user)
        return db_user
    return None

def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return db_user
    return None

def get_all_users(db: Session):
    return db.query(models.User).all()

# Создание задачи
def create_task(db: Session, title: str, description: str, deadline: date, priority: int, user_id: int):
    new_task = models.Task(title=title, description=description, deadline=deadline, priority=priority, user_id=user_id)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

# Получение задачи по идентификатору
def get_task(db: Session, task_id: int):
    return db.query(models.Task).filter(models.Task.id == task_id).first()

# Получение всех задач
def get_all_tasks(db: Session):
    return db.query(models.Task).all()

# Обновление задачи
def update_task(db: Session, task_id: int, title: str, description: str, deadline: date, priority: int):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if task:
        task.title = title
        task.description = description
        task.deadline = deadline
        task.priority = priority
        db.commit()
        db.refresh(task)
    return task

# Удаление задачи
def delete_task(db: Session, task_id: int):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if task:
        db.delete(task)
        db.commit()
    return task
