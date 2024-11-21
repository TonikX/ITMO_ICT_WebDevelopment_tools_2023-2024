from fastapi import FastAPI, HTTPException, Depends
from typing import List
from sqlmodel import Session, select

from connection import init_db, get_session
from models import Task, Category, Tag, TaskDefault, TagDefault, CategoryDefault

app = FastAPI()


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/tasks", response_model=List[Task])
def get_tasks(session: Session = Depends(get_session)):
    tasks = session.exec(select(Task))
    return tasks.all()


@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.post("/tasks", response_model=Task)
def create_task(task_data: TaskDefault, session: Session = Depends(get_session)):
    new_task = Task(**task_data.dict())
    session.add(new_task)
    session.commit()
    session.refresh(new_task)
    return new_task


@app.patch("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task_data: TaskDefault, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task_data_dict = task_data.dict(exclude_unset=True)
    for key, value in task_data_dict.items():
        setattr(task, key, value)

    session.commit()
    session.refresh(task)
    return task


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    session.delete(task)
    session.commit()
    return {"status": "Task deleted"}


@app.get("/tags", response_model=List[Tag])
def get_tags(session: Session = Depends(get_session)):
    tags = session.exec(select(Tag))
    return tags.all()


@app.get("/tags/{tag_id}", response_model=Tag)
def get_tag(tag_id: int, session: Session = Depends(get_session)):
    tag = session.get(Tag, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag


@app.post("/tags", response_model=Tag)
def create_tag(tag_data: TagDefault, session: Session = Depends(get_session)):
    new_tag = Tag(**tag_data.dict())
    session.add(new_tag)
    session.commit()
    session.refresh(new_tag)
    return new_tag


@app.patch("/tags/{tag_id}", response_model=Tag)
def update_tag(tag_id: int, tag_data: TagDefault, session: Session = Depends(get_session)):
    tag = session.get(Tag, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")

    tag_data_dict = tag_data.dict(exclude_unset=True)
    for key, value in tag_data_dict.items():
        setattr(tag, key, value)

    session.commit()
    session.refresh(tag)
    return tag


@app.delete("/tags/{tag_id}")
def delete_tag(tag_id: int, session: Session = Depends(get_session)):
    tag = session.get(Tag, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")

    session.delete(tag)
    session.commit()
    return {"status": "Tag deleted"}


@app.get("/categories", response_model=List[Category])
def get_categories(session: Session = Depends(get_session)):
    categories = session.exec(select(Category))
    return categories.all()


@app.get("/categories/{category_id}", response_model=Category)
def get_category(category_id: int, session: Session = Depends(get_session)):
    category = session.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@app.post("/categories", response_model=Category)
def create_category(category_data: CategoryDefault, session: Session = Depends(get_session)):
    new_category = Category(**category_data.dict())
    session.add(new_category)
    session.commit()
    session.refresh(new_category)
    return new_category


@app.patch("/categories/{category_id}", response_model=Category)
def update_category(category_id: int, category_data: CategoryDefault, session: Session = Depends(get_session)):
    category = session.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    category_data_dict = category_data.dict(exclude_unset=True)
    for key, value in category_data_dict.items():
        setattr(category, key, value)

    session.commit()
    session.refresh(category)
    return category


@app.delete("/categories/{category_id}")
def delete_category(category_id: int, session: Session = Depends(get_session)):
    category = session.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    session.delete(category)
    session.commit()
    return {"status": "Category deleted"}
