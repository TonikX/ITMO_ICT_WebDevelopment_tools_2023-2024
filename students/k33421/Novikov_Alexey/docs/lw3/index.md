# Docker. Упаковка FastAPI приложения в Docker, Работа с источниками данных и Очереди

Цель: Научиться упаковывать FastAPI приложение в Docker, интегрировать парсер данных с базой данных и вызывать парсер через API и очередь.

<a href="https://github.com/TonikX/ITMO_ICT_WebDevelopment_tools_2023-2024?tab=readme-ov-file#%D0%BB%D0%B0%D0%B1%D0%BE%D1%80%D0%B0%D1%82%D0%BE%D1%80%D0%BD%D0%B0%D1%8F-%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%B0-3-%D1%83%D0%BF%D0%B0%D0%BA%D0%BE%D0%B2%D0%BA%D0%B0-fastapi-%D0%BF%D1%80%D0%B8%D0%BB%D0%BE%D0%B6%D0%B5%D0%BD%D0%B8%D1%8F-%D0%B2-docker-%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%B0-%D1%81-%D0%B8%D1%81%D1%82%D0%BE%D1%87%D0%BD%D0%B8%D0%BA%D0%B0%D0%BC%D0%B8-%D0%B4%D0%B0%D0%BD%D0%BD%D1%8B%D1%85-%D0%B8-%D0%BE%D1%87%D0%B5%D1%80%D0%B5%D0%B4%D0%B8" class="external-link" target="_blank">Текст работы</a>

Начнём с подготовки к упаковке ранее созданного приложения в Docker.

Создадим новую директорию, в которую поместим непосредственно директорию с приложением.

В PyCharm выставим директорию с приложением к Sources Root, так как в будущем Docker контейнере она будет являться корнем.  
Исправим все импорты во всех файлах, чтобы они начинались от нового корня.

Теперь в "основном" корне (где у нас лежит директория с приложением) скопируем `.env` файл и создадим новый файл `requirements.txt`, 
в котором перечислим используемые нами библиотеки их версии:

```title="requirements.txt"
alembic==1.13.1
fastapi[all]==0.111.0
SQLAlchemy==2.0.30
psycopg[c]==3.1.19
python-dotenv==1.0.1
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
```

Здесь же создадим файл `Dockerfile`, в котором опишем образ, который будет использоваться для нашего приложения.  
Для экономии места будем использовать многоступенчатый build.

В первой ступени опишем шаги, общие для всех остальных: установим директорию `/app` рабочей, скопируем файл `requirements.txt` 
и выставим значения для переменных окружения Python.

Во второй ступени установим необходимые для компилирования библиотек пакеты, установим пакетный менеджер `uv`, с его 
помощью создадим виртуальное окружение и установим все пакеты из `requirements.txt`.

На третьей ступени установим пакет, необходимый для работы с БД, скопируем виртуальное окружение из предыдущей ступени 
и скопируем все файлы из директории с приложением.

```dockerfile title="Dockerfile"
--8<-- "lr3/Dockerfile"
```

Теперь создадим `docker-compose.yml`, в котором опишем контейнер, который будет создаваться на основе нашего образа, а также 
создадим контейнер для БД:

```yaml title="docker-compose.yml"
version: "3.4"

services:
  db:
    image: postgres:14.1
    hostname: ${DATABASE__HOST}
    container_name: db
    restart: always
    volumes:
      - ./db_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_USER=${DATABASE__USER}
      - POSTGRES_PASSWORD=${DATABASE__PASSWORD}
      - POSTGRES_DB=${DATABASE__NAME}
    env_file:
      - .env

  rest:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: rest
    command: python -m uvicorn rest.app:app --host 0.0.0.0 --port 8081
    restart: always
    volumes:
      - ./lab/:/app
    ports:
      - "8081:8081"
    env_file:
      - .env
    depends_on:
      - db
```

Для БД будем использовать официальный образ `postgres`, hostname и данные авторизации будем использовать из переменных окружения, 
чтобы потом в приложении использовать те же данные (эта часть уже настроена мной в первой лабораторной работе).

Для приложения за основу возьмём написанный нами образ, напишем команду для запуска сервера, укажем `volumes`, который 
соответствует местонахождению приложения локально и в докере, чтобы при перезапуске контейнера не приходилось заново строить контейнер. 
Раскроем порт, через который будем подключаться с нашей машины и укажем используемый `.env` файл.

В файле подключения к БД нужно заменить `localhost` на указанный `DATABASE__HOST`.

Теперь наше приложение работает так же, как и ранее, но через Docker.

Для интеграции парсера в наше приложение нужно написать модуль для настройки и запуска Celery, а также написать там 
задачу, которая будет запускать парсер. И всё это нужно обернуть в Docker.

Добавим в файл `requirements.txt` новую зависимость:

```title="requirements.txt"
...
celery[redis]==5.4.0
```

Добавим в `docker-compose.yml` два новых контейнера: RabbitMQ и Redis. Первый будет выступать для Celery брокером сообщений, 
а второй будет хранить результаты выполнения задач.

```yaml title="docker-compose.yml"
version: "3.4"

services:
  ...

  rabbitmq:
    image: rabbitmq:3.13.1
    hostname: ${RABBITMQ__HOST}
    container_name: rabbitmq
    restart: always

  redis:
    image: redis:7.2.4
    hostname: ${REDIS__HOST}
    container_name: redis
    restart: always
```

Добавим `host` для каждого в `.env` файл и в `config.py`. Конфиг сейчас выглядит следующим образом:

```python title="config.py"
--8<-- "lr3/lab/config.py"
```

В директории с приложением создадим новую директорию для Celery и создадим там модуль для подключения Celery и задачи для парсинга:

```python title="celery_tasks/app.py"
--8<-- "lr3/lab/celery_tasks/app.py"
```

Теперь в `docker-compose.yml` создадим контейнер и для Celery. Использовать для него будем тот же образ, что и для основного приложения:

```yaml title="docker-compose.yml"
version: "3.4"

services:
  ...

  celery:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: celery
    command: python -m celery -A celery_tasks.app worker
    restart: always
    volumes:
      - ./lab/:/app
    env_file:
      - .env
    depends_on:
      - rest
      - redis
      - rabbitmq
```

Осталось только добавить в наше приложение новые эндпоинты для работы с этой Celery задачей.

Для этого создадим новый модуль для нового роутера и его схем. В роутере создадим 3 эндпоинта: для запуска задачи, для 
проверки статуса её выполнения и для получения результата:

=== "celery_router/router.py"

    ```Python
    --8<-- "lr3/lab/rest/celery_router/router.py"
    ```

=== "celery_router/schemas.py"

    ```Python
    --8<-- "lr3/lab/rest/celery_router/schemas.py"
    ```

Пересоберём контейнер нашего приложения и порадуемся результатом!