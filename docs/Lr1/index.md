# ЛР1 — FastAPI Time Manager

## Тема
time manager, управление задачами, дедлайнами и учетом времени

## Что реализовано
- fastapi приложение с postgresql
- orm на sqlmodel
- миграции alembic
- типизированные схемы запросов и ответов
- crud для задач, приоритетов, треков времени, расписаний и уведомлений
- вложенные get ответы для связей one-to-many и many-to-many
- авторизация, регистрация, jwt
- хэширование паролей

## Модель данных
- `users`
- `priorities`
- `tasks`
- `time_tracks`
- `schedules`
- `schedule_task_link`
- `notifications`

## Связи
- one-to-many: `users -> tasks`, `priorities -> tasks`, `tasks -> time_tracks`, `users -> schedules`, `users -> notifications`
- many-to-many: `schedules <-> tasks` через `schedule_task_link`
- ассоциативная сущность с доп полями: `planned_start`, `planned_minutes`, `sort_order`

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
- `GET /tasks/{id}`
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
- `GET /schedules/{id}`
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

## Swagger/OpenAPI
- swagger ui: `http://127.0.0.1:8000/docs`
- redoc: `http://127.0.0.1:8000/redoc`
- openapi json в проекте: `students/k3341/Borodin_Maksim/Lr1/docs/openapi.json`

## Ссылки на исходники
- проект: `students/k3341/Borodin_Maksim/Lr1`
- локальная документация студента: `students/k3341/Borodin_Maksim/docs/Lr1/macdocs.md`
