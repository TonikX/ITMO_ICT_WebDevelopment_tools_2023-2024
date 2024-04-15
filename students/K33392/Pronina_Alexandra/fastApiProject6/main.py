from fastapi import FastAPI
import getpass
from contextlib import asynccontextmanager
from database import init_db, get_session, SessionLocal
from models import User
import api as api_router

app = FastAPI()

# Функция для получения сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Асинхронный контекстный менеджер для событий жизненного цикла
@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        init_db()  # Инициализация базы данных перед стартом приложения
        yield
    finally:
        pass  # Можно добавить здесь код для завершения работы приложения, если требуется

app = FastAPI(lifespan=lifespan)  # Передаем функцию событий жизненного цикла в качестве параметра

# Обработчик маршрута для приветствия

@app.get("/")
async def hello():
    username = getpass.getuser()
    return f"Hello, {username}!"

# Подключаем маршруты из модуля api
app.include_router(api_router.router)
