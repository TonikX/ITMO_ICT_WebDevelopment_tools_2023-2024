# Вызов парсера через очередь

`Задача:` Необходимо добавить зависимости для Celery и Redis в проект. Celery будет использоваться для обработки задач в фоне, а Redis будет выступать в роли брокера задач и хранилища результатов.

Приложение Celery и задача для него:

```Python

--8<-- "laboratory_work_3/dockerProject/parser_app/parser/celery_parser.py"
```

Файл main.py приложения парсера

```Python
from fastapi import FastAPI
import uvicorn
from parser.threading_parser import crypto_parse
from parser.settings import URLS

app = FastAPI()

--8<-- "laboratory_work_3/dockerProject/parser_app/main.py:20:27"
```

Файл main.py главного приложения:

```Python
from fastapi import FastAPI, HTTPException, Depends
from connections import init_db, get_session
from sqlalchemy.orm import Session
import requests
import uvicorn

--8<-- "laboratory_work_3/dockerProject/funance_app/main.py:10:27"
```

Добавление в файл docker-compose.yml:

```Python
--8<-- "laboratory_work_3/dockerProject/docker-compose.yml:33:"
```