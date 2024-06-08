**Подзадача 1: Упаковка FastAPI приложения, базы данных и парсера данных в Docker**
**Docker** — это платформа для разработки, доставки и запуска приложений в контейнерах. Контейнеры позволяют упаковать приложение и все его зависимости в единый образ, который можно запускать на любой системе, поддерживающей Docker, что обеспечивает консистентность среды выполнения и упрощает развертывание. Docker помогает ускорить разработку, повысить гибкость и масштабируемость приложений. Материалы: [Основы работы с Docker](https://tproger.ru/translations/docker-for-beginners/).

- Создание FastAPI приложения: Создано в рамках лабораторной работы номер 1
- Создание базы данных: Создано в рамках лабораторной работы номер 1
- Создание парсера данных: Создано в рамках лабораторной работы номер 2

Реулизуйте возможность вызова парсера по http Для этого можно сделать отдельное приложение FastAPI для парсера или воспользоваться библиотекой socket или подобными.

Пример кода:

```
from fastapi import FastAPI, HTTPException
...

app = FastAPI()

@app.post("/parse")
def parse(url: str):
    try:
        response = requests.get(url)
        response.raise_for_status()
        # Вызов парсера
        return {"message": "Parsing completed", ...}
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))
```
- Разработка Dockerfile:

Необходимо создать Dockerfile для упаковки FastAPI приложения и приложения с паресером. В Dockerfile указать базовый образ, установить необходимые зависимости, скопировать исходные файлы в контейнер и определить команду для запуска приложения.

**Зачем:** Docker позволяет упаковать приложение и все его зависимости в единый контейнер, что обеспечивает консистентность среды выполнения и упрощает развертывание.

- Создание Docker Compose файла:

Необходимо написать docker-compose.yml для управления оркестром сервисов, включающих FastAPI приложение, базу данных и парсер данных. Определите сервисы, укажите порты и зависимости между сервисами.

Зачем: Docker Compose упрощает управление несколькими контейнерами, позволяя вам запускать и настраивать все сервисы вашего приложения с помощью одного файла конфигурации.

<hr> 
<hr>
**Dockerfile**
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

Первая версия **docker-compose.yml**
```
services:
  db:
    image: postgres:13
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: 12345678
      POSTGRES_DB: recipes
    ports:
      - "5433:5432" # тут порт пришлось поменять, потому что оно иначе 
    volumes:        # отказывалось со мной сотрудничать
      - postgres_data:/var/lib/postgresql/data

  web:
    build: .
    depends_on:
      - db
      - redis
    environment:
      DATABASE_URL: postgresql://postgres:12345678@db:5432/recipes
    ports:
      - "8080:8000" # тут порт изменен, просто чтоб можно было, интереса ради, 
                    # открывать параллельно проект локально и из докера
    command: ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

  parser:
    build: .
    depends_on:
      - db
      - redis
    environment:
      DATABASE_URL: postgresql://postgres:12345678@db:5432/recipes
    command: ["python", "parser.py"]

volumes:
  postgres_data:



```