# Dockerfile
Для создания Dockerfile воспользуемся реализованным кодом из первой и второй лабораторной работы и сохраним все необходимое в папке Lr3. На основе кода составим requirements.txt и поместим его во внешнюю директорию Chaptykov_Nikolai (Выбор директории обусловлен удобным доступом ко всем используемым ресурсам). 
Установим рабочие директории и загрузим необходимые файлы из Lr3 для образа:
```Python
FROM python:3.12.0

WORKDIR /src

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./Lr3 .

```
Добавим полезные строки. Первая строка заставляет Python не сохранять .pyc файлы, а вторая отключает буфферизацию вывода из Python:
```Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUBUFFERED 1
```
Воспользуемся также директивами --no-cache-dir и --upgrade при установке библиотек, чтобы не кешировать их и при необходимости обновлять.