# Лабораторная работа № 3

Третья лабораторная работа посвящена контейнеризации созданного приложения и налаживанию коммуникации между контейнерами.

## FastAPI-приложение для парсинга

Чтобы обращаться к парсеру по http, было создано небольшое приложение на FastAPI.
```
parser = FastAPI()

@parser.get("/parse")
def parse(url: str):
    with requests.Session() as session:
        response = session.get(url=url, headers={'User-Agent': 'Mozilla/129.0.2'}).json()

    hackathons = []

    for post in response['posts']:
        hackathon = {}

        title = post['title']
        descr = post['descr'].replace("<br />", "").replace("&nbsp;", " ")

        hackathon['name'] = title
        hackathon['description'] = descr

        hackathons.append(hackathon)
    
    return hackathons
```
Метод parse получает на вход url и отправляет на него запрос, а из результата в формате json вычленяет необходимые нам данные.

## Настройка Docker

Для контейнеризации PostgreSQL был использован готовый образ, взятый с Docker Hub. 

### Dockerfile для приложения

```
FROM python:3.11.9

WORKDIR /code

COPY ./app/requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

EXPOSE 8000

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "8000", "app.main:app"]
```

Данный файл указывает родительский образ - python 3.11.9, копирует локальные директории с приложением в контейнер, устанавливает зависимости, открывает порт 8000 и запускает сервер uvicorn, принимающий подключения с любого адреса.

### Dockerfile для парсера

```
FROM python:3.11.9

WORKDIR /code

COPY ./parser/requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./parser /code/parser

EXPOSE 8000

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "8000", "parser.main:parser"]
```

Данный скрипт аналогичен предыдущему, за исключением наименования директорий.

### Docker Compose

Docker Compose поможет нам оркестрировать созданные контейнеры и связать их в одну сеть, чтобы они могли беспрепятственно коммуницировать.

```
services:
  web:
    build:
      context: .
      dockerfile: app.Dockerfile
    container_name: webapp_test
    restart: always
    ports:
      - "8000:8000"
    env_file:
      - /app/.env
    depends_on:
      db:
        condition: service_healthy
    volumes:
      - ./application:/app
```
Первая секция отвечает за веб-приложение, запуская его в контейнере webapp_test. При ошибках контейнер будет перезапускаться. Обращаться к серверу в контейнере можно через внешний порт 8000. Также здесь указана зависимость от контейнера с БД (пока не заработает БД, не запустится и приложение), настроен логический том, в котором будут храниться данные приложения.
```
  parser:
    build:
      context: .
      dockerfile: parser.Dockerfile
    container_name: parser_test
    restart: always
    ports:
      - "8001:8000"
    volumes:
      - ./parser:/parser
```
Подобным образом создается контейнер для парсера, однако здесь не проверяется успешная работа контейнера postgres, поскольку парсер в данном случае будет только собирать и возвращать данные клиенту, но не вносить их в базу. Обращение к парсеру извне будет происходить через внешний порт 8001.
```
  db:
    image: postgres
    container_name: postgres_test
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: 123
      POSTGRES_DB: hackathon_db
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
```
Контейнер с БД задействует предустановленный образ postgres. В переменных окружения находятся данные для доступа к БД. Также реализован автоматический health_check, проверяющий работоспособность базы данных при каждом запуске контейнера.
База данных hackathon_db внутри контейнера создана через командный интерфейс контейнера при помощи psql.

При помощи команды `docker network inspect lab3_default` можно удостовериться, что все три контейнера объединены в одну автоматически созданную сеть lab3_default.

```
 "Containers": {
            "0baed4df798c1fe7fa5dec3038597483b6817b219c5f68a98d8f16ee7d97e607": {
                "Name": "parser_test",
                "EndpointID": "6e6c2085fa70abb022418e361508ecf72997487db86adb3555da539381b6e3bc",
                "MacAddress": "02:42:ac:12:00:02",
                "IPv4Address": "172.18.0.2/16",
                "IPv6Address": ""
            },
            "0fe0fc48d432f243ffe237409e21241cc3f34abcfe26a12317859240fbde494f": {
                "Name": "webapp_test",
                "EndpointID": "5b7fbefd4b0ac2b86e9f274c18e122224f83f1290bc16abb33fc06d55cb7aea3",
                "MacAddress": "02:42:ac:12:00:04",
                "IPv4Address": "172.18.0.4/16",
                "IPv6Address": ""
            },
            "f870e9793f323f27f99fcd9ce881338d74a940665f80afdf694e4c1e80ffff1d": {
                "Name": "postgres_test",
                "EndpointID": "bd5642ac9380a80dfd7efbba82475adc68b4359f94c109611f80cbe646135731",
                "MacAddress": "02:42:ac:12:00:03",
                "IPv4Address": "172.18.0.3/16",
                "IPv6Address": ""
            }
```

Контейнеры успешно пингуются между собой, что также свидетельствует о правильной конфигурации сети. 
Через локалхост можно получить доступ к обоим приложениям и отправлять запросы через REST API, при этом все изменения в базе данных отразятся в контейнере postgresql.

Запрос через API приложения в браузере локалхоста:
```
2024-10-22 14:01:01 INFO:     172.18.0.1:59446 - "POST /team/ HTTP/1.1" 200 OK
```

Изменения в контейнере БД:
```
hackathon_db=# select * from team;
    name     | id 
-------------+----
 sample team |  2
(1 row)
```

## Эндпоинт для вызова парсера 

В приложении FastAPI был создан следующий эндпоинт:

```
@app.get("/parser_call")
def call_parser(url):
    with requests.Session() as session:
        response = session.get(f'http://parser_test:8000/parse?url={url}', headers={'User-Agent': 'Mozilla/129.0.2'})
    return response.json()
```

Он отправляет на внутренний адрес парсера GET-запрос с введенным url, что задействует ранее описанный метод парсера.

Удостоверимся в работоспособности метода.

Запрос из приложения:
```
2024-10-22 14:08:27 INFO:     172.18.0.1:58336 - "GET /parser_call?url=https%3A%2F%2Ffeeds.tildacdn.com%2Fapi%2Fgetfeed%2F%3Ffeeduid%3D131632209651-986950497851 HTTP/1.1" 200 OK
```
Отклик в парсере:
```
2024-10-22 14:08:27 INFO:     172.18.0.4:40434 - "GET /parse?url=https://feeds.tildacdn.com/api/getfeed/?feeduid=131632209651-986950497851 HTTP/1.1" 200 OK
```

## Выводы

Таким образом, в ходе данной лабораторной работы были получены практические навыки работы с Docker и создано мультиконтейнерное приложение на основе FastAPI и PostgreSQL.