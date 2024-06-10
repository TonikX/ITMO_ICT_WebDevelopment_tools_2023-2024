# Упаковка в Docker

Для FastAPI приложения и папсера были написаны отдельные Docker-файлы. 
Заданы рабочие директории, установка зависимостей и команды входа.

## Docker для FastAPI приложения

    FROM python:3.11
    
    WORKDIR /app
    
    COPY requirements.txt .
    
    RUN pip install --root-user-action=ignore -r /app/requirements.txt
    
    COPY . .
    
    ENTRYPOINT [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]


## Docker для парсера данных

    FROM python:3.11
    
    WORKDIR /web_parser
    
    COPY requirements.txt .
    
    RUN pip install --root-user-action=ignore -r /web_parser/requirements.txt
    
    COPY . .
    
    CMD [ "uvicorn", "web_parser:app", "--host", "0.0.0.0", "--port", "8081"]