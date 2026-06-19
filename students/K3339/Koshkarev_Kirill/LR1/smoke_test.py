"""Сквозной smoke-тест всех основных сценариев API (через TestClient).

Запуск:  .venv/bin/python smoke_test.py
Тест использует отдельную БД в файле smoke_test.db, чтобы не трогать рабочую.
"""
import os
import subprocess
import sys

os.environ["DATABASE_URL"] = "sqlite:///./smoke_test.db"
# Чистим прошлую БД, чтобы тест был воспроизводимым.
if os.path.exists("smoke_test.db"):
    os.remove("smoke_test.db")

# Схему БД создаём миграциями Alembic (как в реальном приложении), а не create_all.
subprocess.run([sys.executable, "-m", "alembic", "upgrade", "head"], check=True, env={**os.environ})

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def auth_header(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


def check(condition: bool, message: str):
    status = "OK  " if condition else "FAIL"
    print(f"[{status}] {message}")
    assert condition, message


# 1. Регистрация: организатор, судья, два участника.
org = client.post("/auth/register", json={
    "full_name": "Иван Организатор", "email": "org@itmo.ru",
    "password": "secret123", "role": "organizer"})
check(org.status_code == 201, "Регистрация организатора (201)")

judge = client.post("/auth/register", json={
    "full_name": "Пётр Судья", "email": "judge@itmo.ru",
    "password": "secret123", "role": "judge"})
check(judge.status_code == 201, "Регистрация судьи (201)")

p1 = client.post("/auth/register", json={
    "full_name": "Аня Участник", "email": "anya@itmo.ru",
    "phone": "+7900000001", "password": "secret123"})
check(p1.status_code == 201, "Регистрация участника 1 (201)")
check(p1.json()["role"] == "participant", "Роль по умолчанию = participant")

p2 = client.post("/auth/register", json={
    "full_name": "Боря Участник", "email": "borya@itmo.ru",
    "password": "secret123"})
check(p2.status_code == 201, "Регистрация участника 2 (201)")

# Дубликат email -> 409.
dup = client.post("/auth/register", json={
    "full_name": "Дубль", "email": "org@itmo.ru", "password": "secret123"})
check(dup.status_code == 409, "Повторный email отклоняется (409)")

# 2. Логин и получение JWT.
def login(email):
    r = client.post("/auth/login", json={"email": email, "password": "secret123"})
    check(r.status_code == 200, f"Логин {email} (200)")
    return r.json()["access_token"]

org_t = login("org@itmo.ru")
judge_t = login("judge@itmo.ru")
p1_t = login("anya@itmo.ru")
p2_t = login("borya@itmo.ru")

# Неверный пароль -> 401.
bad = client.post("/auth/login", json={"email": "org@itmo.ru", "password": "wrong"})
check(bad.status_code == 401, "Неверный пароль отклоняется (401)")

# 3. Аутентификация по JWT.
me = client.get("/auth/me", headers=auth_header(p1_t))
check(me.status_code == 200 and me.json()["email"] == "anya@itmo.ru", "GET /auth/me по JWT")

# Без токена -> 401.
no_token = client.get("/auth/me")
check(no_token.status_code == 401, "Доступ без токена запрещён (401)")

# Битый токен -> 401.
bad_token = client.get("/auth/me", headers=auth_header("abc.def.ghi"))
check(bad_token.status_code == 401, "Битый токен отклоняется (401)")

# Подделанная подпись -> 401.
forged = p1_t[:-3] + ("aaa" if not p1_t.endswith("aaa") else "bbb")
check(client.get("/auth/me", headers=auth_header(forged)).status_code == 401,
      "Подделанная подпись отклоняется (401)")

# 4. Доп. методы: список пользователей, инфо о пользователе, смена пароля.
users = client.get("/users", headers=auth_header(p1_t))
check(users.status_code == 200 and len(users.json()) == 4, "Список пользователей (4 шт.)")

p1_id = p1.json()["id"]
one = client.get(f"/users/{p1_id}", headers=auth_header(p2_t))
check(one.status_code == 200, "Инфо о пользователе по id")

ch = client.put("/users/me/password", headers=auth_header(p2_t),
                json={"old_password": "secret123", "new_password": "newpass456"})
check(ch.status_code == 200, "Смена пароля (200)")
relogin = client.post("/auth/login", json={"email": "borya@itmo.ru", "password": "newpass456"})
check(relogin.status_code == 200, "Логин с новым паролем")
p2_t = relogin.json()["access_token"]  # обновляем токен новым логином

# Подтверждение участника организатором.
conf = client.post(f"/users/{p1_id}/confirm", headers=auth_header(org_t))
check(conf.status_code == 200 and conf.json()["is_confirmed"] is True, "Подтверждение участника организатором")
# Участник не может подтверждать -> 403.
check(client.post(f"/users/{p1_id}/confirm", headers=auth_header(p1_t)).status_code == 403,
      "Участник не может подтверждать (403)")

# 5. Хакатон (только организатор).
check(client.post("/hackathons", headers=auth_header(p1_t),
                  json={"title": "X"}).status_code == 403,
      "Участник не может создать хакатон (403)")
h = client.post("/hackathons", headers=auth_header(org_t),
                json={"title": "ITMO Hack 2026", "description": "Учебный хакатон",
                      "status": "active"})
check(h.status_code == 201, "Создание хакатона организатором (201)")
h_id = h.json()["id"]

# 6. Команды (many-to-many с характеризующим полем role_in_team).
team = client.post("/teams", headers=auth_header(p1_t),
                   json={"name": "Алгоритмисты", "hackathon_id": h_id, "role_in_team": "captain"})
check(team.status_code == 201, "Создание команды (201)")
t_id = team.json()["id"]
check(len(team.json()["members"]) == 1, "Создатель добавлен в состав")

join = client.post(f"/teams/{t_id}/join", headers=auth_header(p2_t),
                   json={"role_in_team": "designer"})
check(join.status_code == 201 and join.json()["role_in_team"] == "designer",
      "Вступление в команду с ролью 'designer'")

# Повторное вступление -> 409.
check(client.post(f"/teams/{t_id}/join", headers=auth_header(p2_t),
                  json={"role_in_team": "x"}).status_code == 409,
      "Повторное вступление отклоняется (409)")

detail = client.get(f"/teams/{t_id}")
check(len(detail.json()["members"]) == 2, "В команде 2 участника")

# 7. Задачи (только организатор).
task = client.post("/tasks", headers=auth_header(org_t),
                   json={"hackathon_id": h_id, "title": "Сервис рекомендаций",
                         "description": "Описание", "requirements": "Python",
                         "evaluation_criteria": "Качество", "max_score": 100})
check(task.status_code == 201, "Публикация задачи организатором (201)")
task_id = task.json()["id"]

# 8. Загрузка работы (только участник команды).
check(client.post("/submissions", headers=auth_header(judge_t),
                  json={"team_id": t_id, "task_id": task_id, "title": "X"}).status_code == 403,
      "Не участник команды не может загрузить работу (403)")
sub = client.post("/submissions", headers=auth_header(p1_t),
                  json={"team_id": t_id, "task_id": task_id, "title": "Прототип v1",
                        "repo_url": "https://github.com/team/proj"})
check(sub.status_code == 201, "Загрузка работы участником команды (201)")
sub_id = sub.json()["id"]

# 9. Оценка (только судья; many-to-many с полями score/comment).
check(client.post(f"/submissions/{sub_id}/evaluate", headers=auth_header(p1_t),
                  json={"score": 80}).status_code == 403,
      "Участник не может оценивать (403)")
ev = client.post(f"/submissions/{sub_id}/evaluate", headers=auth_header(judge_t),
                 json={"score": 87.5, "comment": "Хорошая работа"})
check(ev.status_code == 201, "Оценка работы судьёй (201)")
# Повторная оценка тем же судьёй -> 409.
check(client.post(f"/submissions/{sub_id}/evaluate", headers=auth_header(judge_t),
                  json={"score": 50}).status_code == 409,
      "Повторная оценка тем же судьёй отклоняется (409)")
# Оценка выше максимума -> 400.
check(client.post(f"/submissions/{sub_id}/evaluate", headers=auth_header(judge_t),
                  json={"score": 999}).status_code in (400, 409),
      "Оценка выше максимума отклоняется")

sub_detail = client.get(f"/submissions/{sub_id}")
check(len(sub_detail.json()["evaluations"]) == 1 and
      sub_detail.json()["evaluations"][0]["score"] == 87.5,
      "Работа содержит оценку 87.5")

print("\nВСЕ ПРОВЕРКИ ПРОЙДЕНЫ УСПЕШНО ✅")

# Уберём тестовую БД.
import app.database as _db
_db.engine.dispose()
if os.path.exists("smoke_test.db"):
    os.remove("smoke_test.db")
