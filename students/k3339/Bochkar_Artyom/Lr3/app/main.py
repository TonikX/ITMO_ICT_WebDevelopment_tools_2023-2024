from fastapi import FastAPI
from app.db.conection import init_db
from app.crud import user, profile, book, exchange, parser

app = FastAPI(
  title="Book Exchange API",
  description="API для обмена книгами между пользователями",
  version="1.0.0",
  openapi_tags=[
    {
      "name": "Регистрация",
      "description": "Осперации с юзерами",
    },
    {
      "name": "Парсер",
      "description": "Парсинг книг по url",
    },
    {
      "name": "Профили",
      "description": "Операции с профилями пользователей",
    },
    {
      "name": "Книги",
      "description": "Операции с книгами",
    },
    {
      "name": "Обмен",
      "description": "Операции с обменом книгами между пользователями",
    }
  ]
)

@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(user.router, tags=["Регистрация"])
app.include_router(parser.router, tags=["Парсер"])
app.include_router(profile.router, tags=["Профили"])
app.include_router(book.router, tags=["Книги"])
app.include_router(exchange.router, tags=["Обмен"])
