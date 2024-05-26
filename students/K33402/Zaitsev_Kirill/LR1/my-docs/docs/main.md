В данном файле реализованы эндпоинты всего проекта
```python
from typing import List

from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import select, Session
from sqlalchemy.orm import selectinload
from typing_extensions import TypedDict

from connection import init_db, get_session
from models import Category, Task, TaskDefault, CategoryDefault, TasksCategories, Label, LabelDefault, StatusEnum

app = FastAPI()


@app.on_event("startup")
def on_startup():
    init_db()


# Tasks
@app.get("/tasks")
def tasks_list(session=Depends(get_session)) -> List[Task]:
    return session.exec(select(Task)).all()


@app.get("/tasks/{task_id}", response_model=TasksCategories)
def get_task(task_id: int, session=Depends(get_session)) -> Task:
    task = session.get(Task, task_id)
    return task


@app.post("/task")
def create_task(task: TaskDefault, session=Depends(get_session)) -> TypedDict('Response', {"status": int,
                                                                                           "data": Task}):
    task = Task.model_validate(task)
    session.add(task)
    session.commit()
    session.refresh(task)
    return {"status": 200, "data": task}


@app.delete("/task/{task_id}")
def delete_task(task_id: int, session=Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    session.delete(task)
    session.commit()
    return {"ok": True}


@app.patch("/task/{task_id}")
def update_task(task_id: int, task: TaskDefault, session=Depends(get_session)) -> TaskDefault:
    db_tasks = session.get(Task, task_id)
    if not db_tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    tasks_data = task.model_dump(exclude_unset=True)
    for key, value in tasks_data.items():
        setattr(db_tasks, key, value)
    session.add(db_tasks)
    session.commit()
    session.refresh(db_tasks)
    return db_tasks


# Categories
@app.get("/categories")
def categories_list(session=Depends(get_session)) -> List[Category]:
    return session.exec(select(Category)).all()


@app.get("/categories/{category_id}")
def get_category(category_id: int, session=Depends(get_session)) -> Category:
    return session.get(Category, category_id)


@app.post("/category")
def category_create(cat: CategoryDefault, session=Depends(get_session)) -> TypedDict('Response', {"status": int,
                                                                                                  "data": Category}):
    cat = Category.model_validate(cat)
    session.add(cat)
    session.commit()
    session.refresh(cat)
    return {"status": 200, "data": cat}


@app.delete("/category/{category_id}")
def delete_category(category_id: int, session=Depends(get_session)):
    category = session.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    session.delete(category)
    session.commit()
    return {"ok": True}


@app.patch("/category/{category_id}")
def update_task(category_id: int, category: CategoryDefault, session=Depends(get_session)) -> CategoryDefault:
    db_categories = session.get(Category, category_id)
    if not db_categories:
        raise HTTPException(status_code=404, detail="Category not found")
    categories_data = category.model_dump(exclude_unset=True)
    for key, value in categories_data.items():
        setattr(db_categories, key, value)
    session.add(db_categories)
    session.commit()
    session.refresh(db_categories)
    return db_categories


# Labels
@app.get("/labels")
def labels_list(session=Depends(get_session)) -> List[Label]:
    return session.exec(select(Label)).all()


@app.get("/labels/{label_id}")
def get_label(label_id: int, session=Depends(get_session)) -> Label:
    return session.get(Label, label_id)


@app.post("/label")
def label_create(lab: LabelDefault, session=Depends(get_session)) -> TypedDict('Response', {"status": int,
                                                                                            "data": Label}):
    lab = Label.model_validate(lab)
    session.add(lab)
    session.commit()
    session.refresh(lab)
    return {"status": 200, "data": lab}


@app.delete("/label/{label_id}")
def delete_label(label_id: int, session=Depends(get_session)):
    label = session.get(Label, label_id)
    if not label:
        raise HTTPException(status_code=404, detail="Label not found")
    session.delete(label)
    session.commit()
    return {"ok": True}


@app.patch("/label/{label_id}")
def update_label(label_id: int, label: LabelDefault, session=Depends(get_session)) -> LabelDefault:
    db_labels = session.get(Label, label_id)
    if not db_labels:
        raise HTTPException(status_code=404, detail="Label not found")
    categories_data = label.model_dump(exclude_unset=True)
    for key, value in categories_data.items():
        setattr(db_labels, key, value)
    session.add(db_labels)
    session.commit()
    session.refresh(db_labels)
    return db_labels


"""# Attach label to task
@app.post("/task/{task_id}/label/{label_id}")
def attach_label_to_task(task_id: int, label_id: int, session=Depends(get_session)):
    task = session.get(Task, task_id)
    label = session.get(Label, label_id)

    if not task or not label:
        raise HTTPException(status_code=404, detail="Task or Label not found")

    # Проверяем, не прикреплена ли уже метка к этой задаче
    for existing_label in task.labels:
        if existing_label.id == label_id:
            raise HTTPException(status_code=400, detail="Label already attached to the task")

    # Создаем новую связь между задачей и меткой
    label_task_link = LabelTaskLink(label_id=label_id, task_id=task_id)
    session.add(label_task_link)
    session.commit()

    return {"status": 200, "message": "Label attached to the task successfully"}
"""

"""@app.get("/task-with-labels/{task_id}", response_model=Task)
def get_task_with_labels(task_id: int, session=Depends(get_session)):
    # Выбираем задачу (task) с жадной загрузкой меток
    task = session.exec(
        select(Task)
        .options(selectinload(Task.labels))
        .where(Task.id == task_id)
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task
"""


@app.get("/tasks/{task_id}/days-spent", response_model=int)
def get_days_spent_on_task(task_id: int, session=Depends(get_session)) -> int:
    task = session.exec(
        select(Task)
        .where(Task.id == task_id)
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Проверяем, что задача имеет статус "done" и содержит дату изменения статуса на "done"
    if task.status == StatusEnum.done and task.done_date is not None:
        days_spent = (task.done_date - task.created_date).days
        return days_spent
    else:
        raise HTTPException(status_code=404, detail="Days spent not available for this task")

```