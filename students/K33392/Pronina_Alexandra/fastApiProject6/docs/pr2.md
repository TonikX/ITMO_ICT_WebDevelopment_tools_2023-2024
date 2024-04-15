# SQLModel и ORM


## Установка SQLModel

Для начала необходимо было установить библиотеку SQLModel. Выполните следующую команду в вашем виртуальном окружении:

```bash
pip install sqlmodel
```

Кроме того, для работы с базой данных PostgreSQL потребуется драйвер psycopg2-binary. Установите его с помощью следующей команды:

```bash
pip install psycopg2-binary
```

## Подключение к БД и инициализация

Для подключения к базе данных и создания сессий используется файл `connection.py`. Пример подключения к PostgreSQL:

```python
from sqlmodel import SQLModel, Session, create_engine

# Строка подключения к БД
db_url = 'postgresql://username:password@localhost/db_name'
engine = create_engine(db_url, echo=True)

# Функция инициализации БД
def init_db():
    SQLModel.metadata.create_all(engine)

# Функция для получения сессии
def get_session():
    with Session(engine) as session:
        yield session
```

## Создание моделей

Модели данных описываются с использованием SQLModel и аннотаций Python. Пример модели:

```python
from sqlmodel import SQLModel, Field

class User(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True)
    username: str = Field(index=True)
    email: str = Field(index=True, unique=True)
```

## Использование моделей

После создания моделей можно выполнять CRUD-операции с базой данных. Пример использования:

```python
from sqlmodel import select
from connection import get_session
from models import User

# Создание пользователя
def create_user(user_data: dict):
    with get_session() as session:
        user = User(**user_data)
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

# Получение пользователя по ID
def get_user(user_id: int):
    with get_session() as session:
        user = session.get(User, user_id)
        return user

# Обновление пользователя
def update_user(user_id: int, user_data: dict):
    with get_session() as session:
        user = session.get(User, user_id)
        for key, value in user_data.items():
            setattr(user, key, value)
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

# Удаление пользователя
def delete_user(user_id: int):
    with get_session() as session:
        user = session.get(User, user_id)
        session.delete(user)
        session.commit()
```

## Запросы

После реализации таблиц необходимо обновить все ранее созданные эндпоинты. Так как теперь вместо виртуальной базы данных будет использоваться настоящая, то необходимо понять логику взаимодействия с ORM.

Ранее, в файле `connection.py` был создан генератор для получения объекта сессий в БД. Такой объект позволяет выполнять запросы к базе данных через специальные методы библиотек SQLModel и SQLAlchemy.

Для того чтобы получать подобный объект внутри разрабатываемых API-функций необходимо в них указывать параметр `session` с изначальным значением в виде класса `Depends` с аргументом в виде ссылки на генератор `get_session`:

```python
session=Depends(get_session)
Класс Depends отвечает за выполнение внедрения зависимостей в приложениях FastAPI. Класс Depends принимает функцию в качестве аргумента и передается в качестве аргумента функции в маршруте, требуя, чтобы условие зависимости было выполнено до инициализации любой операции внутри тела API-метода. Подробнее о том, как можно работать с зависимостями описано в официальной документации.

Создание объектов
Для реализации POST-запроса, записывающего новый объект воина в БД, необходимо:

Создать новую модель для POST-запросов к объекту.
Обновить изначально разработанный эндпоинт, добавляющий запись воина во временную БД.
Ввиду того, что при создании нового объекта некоторые поля не всегда надо указывать (таким полем может быть, например, первичный ключ), возникает необходимость в добавлении новых моделей, обрабатывающих запросы. Подобные модели, по факту, являются аналогами Pydantic-объектов, сериализирующие данные в ту и другую сторону и в БД не реализуются.

За реализацию конкретной модели в БД отвечает аргумент table=True, при описании класса.

Для модели воина, таким образом, можно реализовать еще одну базовую модель WarriorDefault, не имеющую id и ссылок на многие-ко многим. Также от такой модели можно отнаследоваться основной моделью, реализующейся в базе данных вместо указания в поле наследования SQLModel. В таком случае достаточно дописать недостающие поля.
```
```python

class WarriorDefault(SQLModel):
    race: RaceType
    name: str
    level: int
    profession_id: Optional[int] = Field(default=None, foreign_key="profession.id")

class Warrior(WarriorDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    profession: Optional[Profession] = Relationship(back_populates="warriors_prof")
    skills: Optional[List[Skill]] = Relationship(back_populates="warriors", link_model=SkillWarriorLink)
```
Используя классы WarriorDefault и Warrior, можно переписать POST-запрос /warrior для новой логики:

```python
@app.post("/warrior")
def warriors_create(warrior: WarriorDefault, session=Depends(get_session)) -> TypedDict('Response', {"status": int,
                                                                                                     "data": Warrior}):
    warrior = Warrior.model_validate(warrior)
    session.add(warrior)
    session.commit()
    session.refresh(warrior)
    return {"status": 200, "data": warrior}
```
## Заключение

SQLModel предоставляет удобные средства для работы с базами данных в FastAPI. Используйте его для создания эффективных и масштабируемых веб-приложений.
