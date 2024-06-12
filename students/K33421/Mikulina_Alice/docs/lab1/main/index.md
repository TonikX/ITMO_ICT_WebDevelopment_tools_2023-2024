# main.py

Необходимые импорты
```
from typing_extensions import TypedDict

import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import select

from connection import init_db, get_session
from db.models import *
```

Импорт конечных точек. Код импортирует различные маршрутизаторы (конечные точки) из разных файлов.
```
# Importing put endpoints
from endpoints.users import router as users_router
from endpoints.books import router as books_router
from endpoints.genres import router as genres_router
from endpoints.book_genre import router as book_genre_router
from endpoints.requests import router as requests_router
from endpoints.auth import router as auth_router
```

Приложение FastAPI. Код создает экземпляр приложения FastAPI с именем app.
```
app = FastAPI()
```

Монтирование конечных точек. Код монтирует различные маршрутизаторы (конечные точки) к приложению FastAPI с помощью метода include_router. Каждый маршрутизатор монтируется с определенным префиксом и тегами для лучшей организации.
```
# Mounting our endpoints
app.include_router(auth_router, prefix="", tags=["auth"])
app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(books_router, prefix="/books", tags=["books"])
app.include_router(genres_router, prefix="/genres", tags=["genres"])
app.include_router(book_genre_router, prefix="/bookgenre", tags=["bookgenre"])
app.include_router(requests_router, prefix="/requests", tags=["requests"])
```

Корневая конечная точка. Код определяет корневую конечную точку (/), которая возвращает простое сообщение «Привет, [имя пользователя]!» сообщение.
```
@app.get("/")
def hello():
    return "Hello, [username]!"
```

 Основная функция: код проверяет, запускается ли скрипт напрямую (а не импортируется как модуль), и выполняет следующие действия:
 — Инициализирует базу данных с помощью функции init_db.
 - Запускает сервер Uvicorn для запуска приложения FastAPI, прослушивающего локальный хост: 8000.
```
if __name__ == "__main__":
    init_db()
    uvicorn.run(app, host="localhost", port=8000)
```