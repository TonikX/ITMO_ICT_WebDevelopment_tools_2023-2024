# Приложение

Основной файл приложения, который конфигурирует и запускает FastAPI приложение.

## Конфигурация

### Импортируемые модули
- FastAPI: Основной фреймворк.
- uvicorn: Сервер для запуска приложения.
- init_db: Инициализация базы данных.
- logic_router: Роуты для основных операций.
- auth_router: Роуты для аутентификации.

### Настройка приложения

```python
app = FastAPI()

app.include_router(logic_router, prefix="/api", tags=["main"])
app.include_router(auth_router, prefix="/api/users", tags=["users"])

@app.on_event("startup")
def on_startup():
    init_db()
