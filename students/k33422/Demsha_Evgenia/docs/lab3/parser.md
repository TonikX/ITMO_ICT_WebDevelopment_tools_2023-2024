# Эндпойнт парсера

`Задача:` Необходимо добавить в FastAPI приложение ендпоинт, который будет принимать запросы с URL для парсинга от клиента, отправлять запрос парсеру (запущенному в отдельном контейнере) и возвращать ответ с результатом клиенту.

Файл main.py приложения парсера

```Python
from fastapi import FastAPI
import uvicorn
from parser.threading_parser import crypto_parse
from parser.settings import URLS

app = FastAPI()

--8<-- "laboratory_work_3/dockerProject/parser_app/main.py:14:19"
```

Файл main.py главного приложения:

```Python
from fastapi import FastAPI, HTTPException, Depends
from connections import init_db, get_session
from sqlalchemy.orm import Session
import requests
import uvicorn

--8<-- "laboratory_work_3/dockerProject/finance_app/main.py:28:41"
```