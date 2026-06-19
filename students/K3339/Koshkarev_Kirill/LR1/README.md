# Лабораторная работа №1 — Серверное приложение на FastAPI

**Дисциплина:** Web-разработка
**Вариант:** Создание системы для проведения хакатонов

Серверное приложение для организации и проведения хакатонов: регистрация
участников, формирование команд, публикация задач организаторами, загрузка
работ командами и их оценка судьями.

---

## 1. Стек технологий

- **FastAPI** — веб-фреймворк
- **SQLAlchemy 2.0** — ORM
- **SQLite** — база данных (файл `hackathon.db`, создаётся автоматически)
- **Pydantic v2** — валидация и сериализация
- **uvicorn** — ASGI-сервер

Аутентификация по JWT, разбор заголовка `Authorization`, кодирование/проверка
подписи JWT и хэширование паролей реализованы **вручную**, только средствами
стандартной библиотеки Python (`hashlib`, `hmac`, `base64`, `secrets`). Сторонние
библиотеки для этого не используются.

---

## 2. Запуск

```bash
cd LR1
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

alembic upgrade head      # создать/обновить схему БД миграциями (см. ниже)
uvicorn app.main:app --reload
```

После запуска:
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

### Миграции базы данных (Alembic)

Схема БД создаётся и версионируется миграциями Alembic, а не через
`create_all`. Это стандартный подход: каждое изменение моделей фиксируется
отдельной версией, которую можно накатить (`upgrade`) или откатить (`downgrade`).

```bash
alembic upgrade head                       # применить все миграции
alembic downgrade -1                       # откатить последнюю
alembic current                            # текущая версия схемы
alembic revision --autogenerate -m "..."   # сгенерировать новую миграцию по моделям
```

Конфигурация: [alembic.ini](alembic.ini) и [alembic/env.py](alembic/env.py)
(берёт строку подключения из `app.config` и метаданные из `app.models`).
Готовая стартовая миграция со всеми 7 таблицами лежит в `alembic/versions/`.

### Проверка (сквозной тест всех сценариев)

```bash
.venv/bin/python smoke_test.py
```

Тест проходит весь путь: регистрация → логин → проверка JWT → создание
хакатона → команды → задачи → загрузка работы → оценка, включая проверки прав
доступа и ошибок (401/403/409/400).

---

## 3. Модель данных

7 таблиц. Удовлетворяет всем критериям задания:

| Таблица | Назначение |
|---|---|
| `users` | участники, организаторы, судьи |
| `hackathons` | хакатоны |
| `teams` | команды (привязаны к хакатону) |
| `team_members` | **ассоциативная** сущность связи User ↔ Team |
| `tasks` | задачи хакатона |
| `submissions` | загруженные работы команд |
| `evaluations` | **ассоциативная** сущность связи Submission ↔ User(судья) |

### Связи

- **one-to-many:**
  - `Hackathon` → `Task` (один хакатон — много задач)
  - `Hackathon` → `Team` (один хакатон — много команд)
  - `Team` → `Submission` (одна команда — много работ)
  - `Task` → `Submission` (одна задача — много работ)
- **many-to-many:**
  - `User` ↔ `Team` через `team_members`
  - `User`(судья) ↔ `Submission` через `evaluations`

### Ассоциативные сущности с характеризующим связь полем

- `team_members.role_in_team` — роль участника в команде (капитан, разработчик,
  дизайнер и т.д.);
- `evaluations.score` и `evaluations.comment` — оценка и комментарий судьи.

```
users ──< team_members >── teams ──< submissions >── tasks
  │                          │            │            │
  │                          └──< (hackathon) >─── hackathons
  └──< evaluations >── submissions
```

---

## 4. Реализация задания на 15 баллов (функционал пользователя)

| Пункт | Где реализовано |
|---|---|
| Авторизация и регистрация | `app/routers/auth.py` (`/auth/register`, `/auth/login`) |
| Генерация JWT-токенов | `app/security.py` → `create_access_token` (вручную, HS256) |
| **Аутентификация по JWT (вручную)** | `app/deps.py` → `get_current_user` + `app/security.py` → `decode_access_token` |
| Хэширование паролей | `app/security.py` → `hash_password` / `verify_password` (PBKDF2-HMAC-SHA256) |
| Инфо о пользователе | `GET /auth/me`, `GET /users/{id}` |
| Список пользователей | `GET /users` |
| Смена пароля | `PUT /users/me/password` |

**Почему аутентификация «ручная».** В `app/deps.py` заголовок
`Authorization: Bearer <token>` разбирается самостоятельно (без
`fastapi.security.OAuth2PasswordBearer`), а подпись и срок действия токена
проверяются собственной функцией `decode_access_token`, которая пересчитывает
HMAC-SHA256 и сравнивает его с подписью из токена (`hmac.compare_digest`).

---

## 5. Список эндпоинтов

### Авторизация
| Метод | Путь | Описание | Доступ |
|---|---|---|---|
| POST | `/auth/register` | Регистрация | все |
| POST | `/auth/login` | Логин, выдача JWT | все |
| GET | `/auth/me` | Текущий пользователь | JWT |

### Пользователи
| Метод | Путь | Описание | Доступ |
|---|---|---|---|
| GET | `/users` | Список пользователей | JWT |
| GET | `/users/{id}` | Пользователь по id | JWT |
| PUT | `/users/me/password` | Смена пароля | JWT |
| POST | `/users/{id}/confirm` | Подтвердить регистрацию | организатор |

### Хакатоны
| Метод | Путь | Описание | Доступ |
|---|---|---|---|
| POST | `/hackathons` | Создать | организатор |
| GET | `/hackathons` | Список | все |
| GET | `/hackathons/{id}` | Один хакатон | все |
| DELETE | `/hackathons/{id}` | Удалить | организатор |

### Команды
| Метод | Путь | Описание | Доступ |
|---|---|---|---|
| POST | `/teams` | Создать команду | JWT |
| GET | `/teams` | Список команд | все |
| GET | `/teams/{id}` | Команда с составом | все |
| POST | `/teams/{id}/join` | Вступить (с ролью) | JWT |
| DELETE | `/teams/{id}/leave` | Выйти из команды | JWT |

### Задачи
| Метод | Путь | Описание | Доступ |
|---|---|---|---|
| POST | `/tasks` | Опубликовать задачу | организатор |
| GET | `/tasks` | Список (фильтр по хакатону) | все |
| GET | `/tasks/{id}` | Одна задача | все |

### Работы и оценки
| Метод | Путь | Описание | Доступ |
|---|---|---|---|
| POST | `/submissions` | Загрузить работу | участник команды |
| GET | `/submissions` | Список работ | все |
| GET | `/submissions/{id}` | Работа с оценками | все |
| POST | `/submissions/{id}/evaluate` | Оценить работу | судья |

---

## 6. Роли пользователей

- `participant` — участник (по умолчанию): создаёт/вступает в команды, загружает работы;
- `organizer` — организатор: создаёт хакатоны, публикует задачи, подтверждает регистрацию;
- `judge` — судья: оценивает работы.

---

## 7. Пример использования (curl)

```bash
# Регистрация участника
curl -X POST http://127.0.0.1:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"full_name":"Аня","email":"anya@itmo.ru","password":"secret123"}'

# Логин -> получаем access_token
curl -X POST http://127.0.0.1:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"anya@itmo.ru","password":"secret123"}'

# Запрос с JWT
curl http://127.0.0.1:8000/auth/me \
  -H "Authorization: Bearer <access_token>"
```

---

## 8. Структура проекта

```
LR1/
├── app/
│   ├── main.py            # точка входа, подключение роутеров
│   ├── config.py          # настройки (БД, секрет JWT, TTL токена)
│   ├── database.py        # engine, сессия, Base, get_db
│   ├── models.py          # 7 моделей SQLAlchemy
│   ├── schemas.py         # Pydantic-схемы
│   ├── security.py        # хэширование паролей + JWT (вручную)
│   ├── deps.py            # ручная аутентификация по JWT, проверка ролей
│   └── routers/
│       ├── auth.py        # регистрация, логин, /me
│       ├── users.py       # список/инфо/смена пароля/подтверждение
│       ├── hackathons.py  # CRUD хакатонов
│       ├── teams.py       # команды и состав (many-to-many)
│       ├── tasks.py       # задачи хакатона
│       └── submissions.py # работы и их оценка (many-to-many)
├── smoke_test.py          # сквозной тест сценариев
├── requirements.txt
└── README.md
```
