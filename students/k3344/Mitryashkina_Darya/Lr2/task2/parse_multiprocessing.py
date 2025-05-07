import multiprocessing
import requests
from bs4 import BeautifulSoup
from time import time
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from db.models import Task, Category, SQLModel
import os
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv("DB_ADMIN").replace("+asyncpg", "")
engine = create_engine(db_url, echo=True)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

def init_db_and_categories():
    SQLModel.metadata.create_all(engine)
    session = SessionLocal()
    session.execute(text("DELETE FROM taskcategory"))
    session.execute(text("DELETE FROM task"))
    for name in ["Answered", "Unanswered"]:
        if not session.query(Category).filter_by(name=name).first():
            session.add(Category(name=name))
    session.commit()
    session.close()

def parse_and_save(url):
    # каждый процесс создает СВОЮ сессию
    session = SessionLocal()
    resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(resp.text, "html.parser")
    questions = soup.select(".s-post-summary")

    for q in questions:
        title_tag = q.select_one(".s-post-summary--content-title")
        desc_tag  = q.select_one(".s-post-summary--content-excerpt")
        title  = title_tag.text.strip() if title_tag else "Без названия"
        descr  = desc_tag.text.strip()  if desc_tag  else "Без описания"

        answers_block = q.select_one(".s-post-summary--stats-item")
        num_tag = answers_block.select_one(".s-post-summary--stats-item-number") if answers_block else None
        num = int(num_tag.text.strip()) if num_tag and num_tag.text.strip().isdigit() else 0

        category_name = "Answered" if num > 0 else "Unanswered"
        category = session.query(Category).filter_by(name=category_name).first()

        task = Task(title=title, description=descr, user_id=1)
        task.categories.append(category)
        session.add(task)
        session.commit()
        print(f"[PROCESS] {title} → {category_name}")

    session.close()

def main():
    multiprocessing.set_start_method("spawn")
    init_db_and_categories()
    pages = 20
    urls = [f"https://stackoverflow.com/questions?tab=newest&page={i}" for i in range(1, pages+1)]

    start = time()
    with multiprocessing.Pool(processes=8) as pool:
        pool.map(parse_and_save, urls)
    print(f"[PROCESS] Время выполнения: {time() - start:.2f} секунд")

if __name__ == "__main__":
    main()

# [PROCESS] Время выполнения: 10.79 секунд