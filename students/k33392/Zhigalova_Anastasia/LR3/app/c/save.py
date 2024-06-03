from sqlalchemy.orm import Session
from app.models import Task, Category

def save_to_db(db: Session, title: str, description: str, priority: int, due_date: str, categories_names: list):
    task = Task(title=title, description=description, priority=priority, due_date=due_date)

    for category_name in categories_names:
        category = db.query(Category).filter_by(name=category_name).first()
        if not category:
            category = Category(name=category_name)
            db.add(category)
            db.commit()

        task.categories.append(category)

    db.add(task)
    db.commit()