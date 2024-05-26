# база - официальный образ python
FROM python:3.8

# создание рабочей директории
WORKDIR /docker_code

# копируем файл с зависимостями в рабочую директорию
COPY ./requirements.txt /docker_code/requirements.txt

# устанавливаем зависимости
RUN pip install --no-cache-dir --upgrade -r /docker_code/requirements.txt

# копируем папку с кодом приложения в рабочую директорию
COPY ./app /docker_code/app

# запускаем приложение в рабочей директории
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]


# создание образа
# docker build -t mainapp_image .

# запуск контейнера
# docker run -d --name mainapp_container -p 8000:8000 mainapp_image