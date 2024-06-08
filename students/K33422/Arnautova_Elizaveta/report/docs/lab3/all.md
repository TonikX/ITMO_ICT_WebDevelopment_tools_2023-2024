Dockerfile
```
FROM python:3.9-slim

WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/requirements.txt

# Install the dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the rest of the working directory contents into the container
COPY . /app

# Expose the port the app runs on
EXPOSE 8000

# Define the command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

docker-compose.yml
```
services:
  db:
    image: postgres:13
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: 12345678
      POSTGRES_DB: recipes
    ports:
      - "5433:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  web:
    build: .
    depends_on:
      - db
      - redis
    environment:
      DATABASE_URL: postgresql://postgres:12345678@db:5432/recipes
    ports:
      - "8080:8000"
    command: ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

  parser:
    build: .
    depends_on:
      - db
      - redis
    environment:
      DATABASE_URL: postgresql://postgres:12345678@db:5432/recipes
    command: ["python", "parser.py"]

  redis:
    image: "redis:alpine"
    ports:
      - "6379:6379"

  worker:
    build: .
    depends_on:
      - db
      - redis
    environment:
      DATABASE_URL: postgresql://postgres:12345678@db:5432/recipes
    command: ["celery", "-A", "tasks.celery_app", "worker", "--loglevel=info"]

  pgadmin:
    image: dpage/pgadmin4
    environment:
      PGADMIN_DEFAULT_EMAIL: admin@admin.com
      PGADMIN_DEFAULT_PASSWORD: admin
    ports:
      - "5050:80"
    depends_on:
      - db

volumes:
  postgres_data:
```

celery_config.py
```
from celery import Celery

celery_app = Celery(
    "tasks",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0"
)

celery_app.conf.task_routes = {
    "tasks.parse_url": {"queue": "parser_queue"},
}

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
)
```

tasks.py
```
from celery_config import celery_app
from sqlalchemy.orm import Session
from connection import SessionLocal
from parser import parse_and_save

@celery_app.task
def parse_url_task(url: str):
    db: Session = SessionLocal()
    try:
        parse_and_save(url, db)
    finally:
        db.close()
```

main.py
```
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
```

parser.py
```
from bs4 import BeautifulSoup
import requests
import re
from sqlalchemy.orm import Session
from models import Author, Title, Category


def parse_and_save(url: str, db: Session):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    recipe_blocks = soup.find_all('div', class_='emotion-etyz2y')

    for block in recipe_blocks:
        try:
            title = block.find('span', class_="emotion-1bs2jj2").text
            ingredients_text = block.find('button', class_="emotion-d6nx0p").text
            servings_text = block.find('span', class_="emotion-tqfyce").text
            cook_time = block.find('span', class_="emotion-14gsni6").text
            author_block = block.find('div', class_="emotion-ah73gc")
            author_name = author_block.find('span', class_="emotion-14tqfr").text.replace("Автор:", "").strip()
            author_link = author_block.find('a')['href']
            author_url = f"https://eda.ru{author_link}"  # Создаем полный URL для автора
            servings = int(re.search(r'\d+', servings_text).group())
            ingredients = int(re.search(r'\d+', ingredients_text).group())

            # Найти URL рецепта
            recipe_link = block.find('a', class_="emotion-18hxz5k")
            if recipe_link:
                recipe_url = recipe_link['href']
                cur_url = f"https://eda.ru{recipe_url}"  # Добавить базовый URL
            else:
                cur_url = None

            # Вставить данные автора и получить его id
            author = db.query(Author).filter_by(name=author_name).first()
            if not author:
                author = Author(name=author_name, author_url=author_url)
                db.add(author)
                db.commit()
                db.refresh(author)

            author_id = author.id

            # Вставить данные рецепта с id автора
            title_entry = Title(
                url=url,
                title=title,
                ingredients=ingredients,
                servings=servings,
                cook_time=cook_time,
                author_id=author_id,
                cur_url=cur_url
            )
            db.add(title_entry)
            db.commit()
            db.refresh(title_entry)

            # Парсинг и вставка категорий
            categories_block = block.find('ul', class_='emotion-1mceoyq')
            if categories_block:
                categories = categories_block.find_all('li')
                for category in categories:
                    category_name = category.find('span', class_='emotion-1h6i17m').text
                    category_link = category.find('a')['href']
                    category_url = f"https://eda.ru{category_link}"

                    # Вставить данные категории и получить ее id
                    category_entry = db.query(Category).filter_by(name=category_name).first()
                    if not category_entry:
                        category_entry = Category(name=category_name, url=category_url)
                        db.add(category_entry)
                        db.commit()
                        db.refresh(category_entry)

                    # Вставить связь между рецептом и категорией
                    title_entry.categories.append(category_entry)
                    db.commit()

        except AttributeError as e:
            print(f"Failed to parse block: {e}")
```