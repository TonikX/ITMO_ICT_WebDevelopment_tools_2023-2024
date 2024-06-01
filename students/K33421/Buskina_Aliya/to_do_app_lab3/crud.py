import datetime
from datetime import date
from typing import List
import aiohttp
import asyncpg
import asyncio
from sqlalchemy.orm import Session
import models
import schemas
#from auth import auth


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

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

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

def get_user_tasks(db: Session, user_id: int):
    return db.query(models.Task).filter(models.Task.user_id == user_id).all()

def get_user_by_task_id(db: Session, task_id: int):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        return None
    return task.owner

def get_tasks_with_time_logs(db: Session, task_id: int):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        return None
    return [{"task": task, "time_logs": task.time_logs}]

def add_time_log(db: Session, task_id: int, time_spent_minutes: int, date_logged: date):
    time_log = models.TimeLog(task_id=task_id, time_spent_minutes=time_spent_minutes, date_logged=date_logged)
    db.add(time_log)
    db.commit()
    db.refresh(time_log)
    return time_log

def get_time_logs_for_task(db: Session, task_id: int):
    return db.query(models.TimeLog).filter(models.TimeLog.task_id == task_id).all()


def get_user_tasks_with_time_logs(db: Session, user_id: int) -> List[schemas.TaskWithTimeLogs]:
    # Получаем все задачи пользователя
    user_tasks = db.query(models.Task).filter(models.Task.user_id == user_id).all()

    tasks_with_time_logs = []
    # Для каждой задачи получаем время, проведенное на ней
    for task in user_tasks:
        time_logs = db.query(models.TimeLog).filter(models.TimeLog.task_id == task.id).all()
        tasks_with_time_logs.append({
            "task": task,
            "time_logs": time_logs
        })

    return tasks_with_time_logs

async def save_to_db(data):
    conn = await asyncpg.connect('postgresql://postgres:Aliya2103@localhost:5432/todo')
    try:
        for record in data:
            deadline = datetime.datetime.strptime(record['deadline'], '%Y-%m-%d').date() if record['deadline'] else None
            await conn.execute(
                "INSERT INTO task (title, description, deadline) VALUES ($1, $2, $3)",
                record['title'], record['description'], deadline
            )
    finally:
        await conn.close()
    return data  # Возвращаем сохраненные данные

async def dict_to_sentence(dictionary):
    sentence_words = [''] * (max(max(indices) for indices in dictionary.values()) + 1)
    for word, indices in dictionary.items():
        for index in indices:
            sentence_words[index] = word
    return ' '.join(sentence_words)

async def parse_and_save(url):
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        async with session.get(url) as response:
            page_with_results = await response.json()
            all_data = []
            if 'results' in page_with_results:
                for result in page_with_results['results']:
                    primary_topic = result.get('primary_topic')
                    if primary_topic:
                        domain_display_name = primary_topic.get('domain', {}).get('display_name', '')
                    else:
                        domain_display_name = ''
                    if domain_display_name:
                        title = result.get('title')
                        if title:
                            record = {'title': domain_display_name,
                                      'deadline': result.get('publication_date', '')}
                            for key, value in result.items():
                                if key not in ['id', 'title', 'publication_date']:
                                    record[key] = value
                            if 'abstract_inverted_index' in result and result['abstract_inverted_index']:
                                record['description'] = await dict_to_sentence(result['abstract_inverted_index'])
                                all_data.append(record)
            saved_data = await save_to_db(all_data)
            return saved_data

async def parse_and_save_to_db(start_page: int, end_page: int):
    urls = [f'https://api.openalex.org/works?page={i}&per-page=200' for i in range(start_page, end_page + 1)]
    tasks = [parse_and_save(url) for url in urls]
    results = await asyncio.gather(*tasks)
    all_results = [item for sublist in results for item in sublist]
    return all_results  # Возвращаем все сохраненные данные
