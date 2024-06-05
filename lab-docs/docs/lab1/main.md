# backend для планера задач на fastAPI

[Ссылка на github](https://github.com/VsevolodKozlov-git/ITMO_ICT_WebDevelopment_tools_2023-2024/tree/lab1/task1/LaboratoryPart)

## Технологии

* FastAPI - backend framework
* SQLModel - ORM
* Alembic - система миграций
* PostgreSQL - SQL база данных
* jose - для работы с JWT токенами
* passlib - для алгоритмов шифрования


## Задача

Реализовать планер с со следующи функционалом:

* Создание проектов
* Добавление пользователей с разными правами:
    * Читатель
    * Редактор
* Изменение проектов
* Добавление категорий в проекты
* Добавление задач в категории
* Добавление сроков и срочности для задач
* Добавление в календарь промежутка выполнения для задачи(дата,  время начала, время конца)
* Подсчет времени, потраченного на задачу, из записей в календаре
* Вывод данных о предстоящих дедлайнах


## Реализация
[Ссылка на github](https://github.com/VsevolodKozlov-git/ITMO_ICT_WebDevelopment_tools_2023-2024/tree/lab1/task1/LaboratoryPart)

## Результат
* Схема БД со следующей архитектурой


|![](static/db.png) |
|:--:|
|Архитектура БД|

* 22 входные точки. Входные точки можно посмотреть [здесь](https://github.com/VsevolodKozlov-git/ITMO_ICT_WebDevelopment_tools_2023-2024/blob/lab1/task1/LaboratoryPart/endpoints/endpoints.py)

