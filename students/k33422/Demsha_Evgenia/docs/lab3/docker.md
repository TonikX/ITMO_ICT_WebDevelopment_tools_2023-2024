# Упаковка в Docker

`Задача:`  Необходимо создать Dockerfile для упаковки FastAPI приложения и приложения с паресером. В Dockerfile указать базовый образ, установить необходимые зависимости, скопировать исходные файлы в контейнер и определить команду для запуска приложения.

Dockerfile для приложения учета личных финансов

```Python
--8<-- "laboratory_work_3/dockerProject/finance_app/Dockerfile"
```

Dockerfile для приложения парсера

```Python
--8<-- "laboratory_work_3/dockerProject/parser_app/Dockerfile"
```

docker-compose.yml
```Python
--8<-- "laboratory_work_3/dockerProject/docker-compose.yml::33"
```
