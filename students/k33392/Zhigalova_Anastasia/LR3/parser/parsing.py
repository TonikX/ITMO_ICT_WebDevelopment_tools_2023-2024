import requests
import chardet
from bs4 import BeautifulSoup
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException
from models import Task, Category, TaskCategory
import traceback

month_number = {
    "января": 1,
    "февраля": 2,
    "марта": 3,
    "апреля": 4,
    "мая": 5,
    "июня": 6,
    "июля": 7,
    "августа": 8,
    "сентября": 9,
    "октября": 10,
    "ноября": 11,
    "декабря": 12
}

def parse_and_save(db: Session, url: str):
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        encoding = chardet.detect(response.content)['encoding']
        response.encoding = encoding
        
        content = response.text
        soup = BeautifulSoup(content, 'html.parser')

        time_element = soup.find('time', class_='D6YRu')
        if time_element:
            date_time_str = time_element['datetime']
            due_date = datetime.fromisoformat(date_time_str.replace('Z', '+00:00'))
        else:
            due_date = datetime.now()

        title = soup.find('title').text.strip()
        
        description_div = soup.find('div', {'data-test': 'RESTRICT-TEXT'})
        description = description_div.get_text().strip() if description_div else ''

        categories_names = [tag.text.strip() for tag in soup.select('a.CjnHd.y8A5E[data-test="LINK"]')]

        value_span = soup.find('span', class_="Value-ie9gjh-2 iZlkBd")
        if value_span is not None:
            value_str = value_span.get_text().split()[0]
            value = float(value_str)

            if value > 8:
                priority = 1
            elif value > 6 and value < 8:
                priority = 2
            else:
                priority = 3
        else:
            priority = 4
            
        save_to_db(db, title, description, priority, due_date, categories_names)

        parsed_data = {
            "title": title,
            "description": description,
            "priority": priority,
            "due_date": due_date.isoformat(),
            "categories": categories_names
        }
        
        return parsed_data
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

def save_to_db(db: Session, title: str, description: str, priority: int, due_date: str, categories_names: list):
    task = Task(title=title, description=description, priority=priority, due_date=due_date)
    db.add(task)
    db.commit()

    for category_name in categories_names:
        category = db.query(Category).filter_by(name=category_name).first()
        if not category:
            category = Category(name=category_name)
            db.add(category)
            db.commit()
        task_category = db.query(TaskCategory).filter_by(category_id = category.id).first()
        if not task_category:
            task_category = TaskCategory(category_id=category.id, additional_info=description, task_id = task.id)
            db.add(task_category)
            db.commit()

    