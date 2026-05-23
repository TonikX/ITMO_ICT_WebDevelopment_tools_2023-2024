# Time Manager API (FastAPI)

простое серверное приложение для управления задачами, временем и расписанием

## Стек
- fastapi
- sqlmodel + postgresql
- alembic
- jwt + passlib bcrypt

## Запуск
1. создать виртуальное окружение и установить зависимости
2. скопировать `.env.example` в `.env` и заполнить значения
3. выполнить миграции
4. запустить сервер

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
alembic upgrade head
uvicorn app.main:app --reload
```

документация swagger будет на `http://127.0.0.1:8000/docs`

## Запуск через docker compose и make
- поднимаем postgres в контейнере, затем миграции и api одной командой

```bash
make install
make up
```

- остановить контейнер бд:

```bash
make down-db
```

## Модели
- `users`
- `priorities`
- `tasks`
- `time_tracks`
- `schedules`
- `schedule_task_link` (many to many + поля связи)
- `notifications`

## Связи
- one to many: user->tasks, priority->tasks, task->time_tracks, user->schedules, user->notifications
- many to many: schedules<->tasks через `schedule_task_link`
- поля связи в link: `planned_start`, `planned_minutes`, `sort_order`

## Эндпоинты

### auth
- `POST /auth/register`
- `POST /auth/login`

### users
- `GET /users`
- `GET /users/me`
- `PATCH /users/me/password`

### priorities
- `GET /priorities`
- `GET /priorities/{id}`
- `POST /priorities`
- `PATCH /priorities/{id}`
- `DELETE /priorities/{id}`

### tasks
- `GET /tasks`
- `GET /tasks/{id}` (вложенный приоритет и треки времени)
- `POST /tasks`
- `PATCH /tasks/{id}`
- `DELETE /tasks/{id}`

### time tracks
- `GET /time-tracks`
- `GET /time-tracks/{id}`
- `POST /time-tracks`
- `PATCH /time-tracks/{id}`
- `DELETE /time-tracks/{id}`

### schedules
- `GET /schedules`
- `GET /schedules/{id}` (вложенные элементы расписания)
- `POST /schedules`
- `PATCH /schedules/{id}`
- `DELETE /schedules/{id}`
- `POST /schedules/{id}/tasks`
- `PATCH /schedules/{id}/tasks/{task_id}`
- `DELETE /schedules/{id}/tasks/{task_id}`

### notifications
- `GET /notifications`
- `GET /notifications/{id}`
- `POST /notifications`
- `PATCH /notifications/{id}`
- `DELETE /notifications/{id}`

## Практики 1.1-1.3
история разделения по этапам готовится через скрипт `scripts/commit_timeline.sh`, он делает последовательность локальных коммитов с датами за последние две недели

## Внешняя структура документации
- сводная папка документации: `students/k3341/Borodin_Maksim/docs`
- документация по этой лабораторной: `students/k3341/Borodin_Maksim/docs/Lr1/macdocs.md`
