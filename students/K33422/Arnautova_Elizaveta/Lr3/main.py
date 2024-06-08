from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from connection import SessionLocal, engine
from models import Base, Author, Title, Category
from dtos import AuthorDTO, TitleOutputDTO, CategoryDTO, UpdateAuthorDTO, UpdateCategoryDTO, UpdateTitleDTO
from typing import List
from parser import parse_and_save
from tasks import parse_url_task
import time

app = FastAPI()

# Создание таблиц
Base.metadata.create_all(bind=engine)


# Зависимость для получения сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/authors/", response_model=List[AuthorDTO])
def read_authors(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    authors = db.query(Author).offset(skip).limit(limit).all()
    return authors


@app.get("/authors/{author_id}", response_model=AuthorDTO)
def read_author(author_id: int, db: Session = Depends(get_db)):
    author = db.query(Author).filter(Author.id == author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@app.get("/titles/", response_model=List[TitleOutputDTO])
def read_titles(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    titles = db.query(Title).offset(skip).limit(limit).all()
    return titles


@app.get("/titles/{title_id}", response_model=TitleOutputDTO)
def read_title(title_id: int, db: Session = Depends(get_db)):
    title = db.query(Title).filter(Title.id == title_id).first()
    if not title:
        raise HTTPException(status_code=404, detail="Title not found")
    return title


@app.get("/categories/", response_model=List[CategoryDTO])
def read_categories(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    categories = db.query(Category).offset(skip).limit(limit).all()
    return categories


@app.get("/categories/{category_id}", response_model=CategoryDTO)
def read_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@app.put("/authors/{author_id}", response_model=AuthorDTO)
def update_author(author_id: int, author_data: UpdateAuthorDTO, db: Session = Depends(get_db)):
    author = db.query(Author).filter(Author.id == author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    for key, value in author_data.dict(exclude_unset=True).items():
        setattr(author, key, value)

    db.commit()
    db.refresh(author)
    return author


@app.put("/titles/{title_id}", response_model=TitleOutputDTO)
def update_title(title_id: int, title_data: UpdateTitleDTO, db: Session = Depends(get_db)):
    title = db.query(Title).filter(Title.id == title_id).first()
    if not title:
        raise HTTPException(status_code=404, detail="Title not found")

    for key, value in title_data.dict(exclude_unset=True).items():
        if key == "category_ids":
            title.categories = db.query(Category).filter(Category.id.in_(value)).all()
        else:
            setattr(title, key, value)

    db.commit()
    db.refresh(title)
    return title


@app.put("/categories/{category_id}", response_model=CategoryDTO)
def update_category(category_id: int, category_data: UpdateCategoryDTO, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    for key, value in category_data.dict(exclude_unset=True).items():
        setattr(category, key, value)

    db.commit()
    db.refresh(category)
    return category


@app.delete("/authors/{author_id}")
def delete_author(author_id: int, db: Session = Depends(get_db)):
    author = db.query(Author).filter(Author.id == author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    db.delete(author)
    db.commit()
    return {"message": "Author deleted successfully"}


@app.delete("/titles/{title_id}")
def delete_title(title_id: int, db: Session = Depends(get_db)):
    title = db.query(Title).filter(Title.id == title_id).first()
    if not title:
        raise HTTPException(status_code=404, detail="Title not found")

    db.delete(title)
    db.commit()
    return {"message": "Title deleted successfully"}


@app.delete("/categories/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    db.delete(category)
    db.commit()
    return {"message": "Category deleted successfully"}


@app.post("/parse/")
def parse_url(url: str, db: Session = Depends(get_db)):
    try:
        parse_and_save(url, db)
        return {"message": "Parser ran successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/сount/")
def count_titles(db: Session = Depends(get_db)):
    titles = db.query(Title).all()
    return {"message": f"Found {len(titles)} recipes"}


# @app.post("/parse/one/async/")
# def parse_url_async(url: str):
#     task = parse_url_task.delay(url)
#     return {"message": "Parsing task started", "task_id": task.id}


@app.post("/parse/async/")
def parse_urls_async(urls: List[str]):
    start_time = time.time()

    task_ids = []
    for url in urls:
        task = parse_url_task.delay(url)
        task_ids.append(task.id)

    end_time = time.time()
    timer = end_time - start_time
    return {"message": "Parsing tasks started", "task_ids": task_ids, "Execution time": f"{timer:.2f}"}


@app.post("/parse/naive/")
def parse_urls_async(urls: List[str], db: Session = Depends(get_db)):
    start_time = time.time()

    for url in urls:
        parse_and_save(url, db)

    end_time = time.time()
    timer = end_time - start_time
    return {"message": "Parsing tasks started", "Execution time": f"{timer:.2f}"}
