## Документация по лабораторной работе №1

### Перечисления (Enums)

### PriorityLevel
Представляет уровень приоритета задачи.

```python
class PriorityLevel(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4
```

### TaskStatus
Предоставляет варианты статусов для задачи в рамках системы.

```python
class TaskStatus(Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    DEFERRED = "deferred"
```

---

## Модели

### TaskScheduleLink
Связывает задачу с расписанием и включает соответствующую информацию о назначении.

```python
class TaskScheduleLink(SQLModel, table=True):
    task_id: int
    schedule_id: int
    assignment_date: datetime
    note: Optional[str]
```

### Task
Определяет свойства задачи, включая ее статус, приоритет, крайний срок, связанного пользователя и связанные анализы времени.

```python
class Task(SQLModel, table=True):
    id: Optional[int]
    title: str
    description: str
    priority: PriorityLevel
    deadline: datetime
    user_id: int
    status: TaskStatus
    created_at: datetime
    updated_at: datetime
    schedules: List["Schedule"]
    user: Optional["User"]
    time_analyses: List["TimeAnalysis"]
```

### User
Представляет пользователя системы. Содержит информацию о задачах пользователя, а также данные для аутентификации.

```python
class User(SQLModel, table=True):
    id: Optional[int]
    username: str
    email: str
    hashed_password: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    tasks: List[Task]
```

### Schedule
Представляет расписание, соответствующее пользователю и список задач.

```python
class Schedule(SQLModel, table=True):
    id: Optional[int]
    date: datetime
    user_id: int
    tasks: List["Task"]
```

### TimeAnalysis
Отслеживает время, затраченное на конкретную задачу.

```python
class TimeAnalysis(SQLModel, table=True):
    id: Optional[int]
    task_id: int
    time_spent: float
    task: Task
```

---

## Схемы

### CreateTask
Схема для создания новой задачи.

```python
class CreateTask(BaseModel):
    title: str
    description: str
    deadline: datetime
    priority: PriorityLevel
    user_id: int
```

### UpdateTask
Схема для обновления информации о существующей задаче.

```python
class UpdateTask(BaseModel):
    title: Optional[str]
    description: Optional[str]
    deadline: Optional[datetime]
    priority: Optional[PriorityLevel]
    time_spent: Optional[float]
    user_id: int
```

### TaskResponse
Схема для представления ответа, содержащего данные задачи.

```python
class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    deadline: datetime
    priority: PriorityLevel
    status: TaskStatus
    user_id: int
    time_spent: float
```

### ScheduleBase
Базовая схема для расписаний.

```python
class ScheduleBase(BaseModel):
    date: datetime
```

### ScheduleResponse
Ответ схемы, который включает задачи, связанные с расписанием.

```python
class ScheduleResponse(ScheduleBase):
    id: int
    tasks: List[TaskResponse]
```

### CreateSchedule
Схема для создания нового расписания со связанными задачами.

```python
class CreateSchedule(ScheduleBase):
    tasks: List[int]
```

### UserCreate
Схема для создания нового пользователя.

```python
class UserCreate(BaseModel):
    username: str
    email: str
    password: str
```

### UserAuthenticate
Схема для входа пользователя.

```python
class UserAuthenticate(BaseModel):
    username: str
    password: str
```

### CreateTimeAnalysis
Схема для создания новой записи анализа времени для задачи.

```python
class CreateTimeAnalysis(BaseModel):
    task_id: int
    time_spent: Optional[float]
```

### TimeAnalysisResponse
Схема для ответа, содержащего данные анализа времени.

```python
class TimeAnalysisResponse(BaseModel):
    id: int
    task_id: int
    time_spent: float
```

Файл `main.py` содержит основной код для обработки запросов и роутинга в приложении. Он включает в себя обработчики запросов для создания, чтения, обновления и удаления задач, расписаний и анализа времени.

### Инициализация базы данных
Функция `init_db()` используется для создания всех таблиц в базе данных при запуске приложения.

### Создание задачи
`create_task()` обработчик POST запроса принимает данные о задаче и создает новую запись в базе данных. Также связывает задачу с текущим пользователем.

### Чтение задач
`read_tasks()` обработчик GET запроса возвращает список всех задач из базы данных.

### Создание расписания
`create_schedule()` обработчик POST запроса создает новое расписание на основе данных, полученных от пользователя. Также связывает задачи с этим расписанием.

### Чтение расписаний
`read_schedules()` обработчик GET запроса возвращает список расписаний текущего пользователя. Можно получить конкретное расписание, указав его ID.

### Обновление задачи
`update_task()` обработчик PATCH запроса обновляет данные о задаче на основе полученных данных от пользователя.

### Удаление задачи
`delete_task()` обработчик DELETE запроса удаляет задачу из базы данных.

### Обновление анализа времени
`update_time_analysis()` обработчик PATCH запроса обновляет данные анализа времени задачи.

### Вспомогательные файлы
`app.py` файл содержит создание и настройку экземпляра FastAPI приложения. 
Используется `CORSMiddleware` для обработки запросов CORS.

`database.py` файл содержит конфигурацию базы данных и создание сессии для взаимодействия с ней.

1. `DATABASE_URL`: Строка подключения к базе данных, полученная из переменных окружения.
2. `engine`: Экземпляр движка базы данных, созданный на основе `DATABASE_URL`.
3. `get_session()`: Функция-генератор, создающая и возвращающая сессию для взаимодействия с базой данных.

### Авторизация
`auth.py` файл содержит обработчики запросов для аутентификации пользователей и выдачи токенов доступа.

### Импорты
1. `JWTError`, `jwt`: Импортируются из `jose`, используются для работы с JWT токенами.
2. `CryptContext`: Импортируется из `passlib.context`, используется для хеширования паролей.
3. `OAuth2PasswordBearer`, `OAuth2PasswordRequestForm`: Импортируются из `fastapi.security`, используются для аутентификации с помощью OAuth2 и получения формы запроса пароля.
4. `secrets`: Импортируется из `secrets`, используется для генерации секретного ключа.

### Основные функции и методы
1. `generate_secret_key(length=32)`: Функция для генерации секретного ключа.
2. `verify_password(plain_password, hashed_password)`: Функция для проверки пароля.
3. `get_password_hash(password)`: Функция для получения хэша пароля.
4. `create_access_token(data: dict, expires_delta: timedelta = None)`: Функция для создания JWT токена доступа.
5. `create_user(user: UserCreate, session: Session = Depends(get_session))`: Обработчик POST запроса для создания пользователя.
6. `login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session))`: Обработчик POST запроса для аутентификации и получения токена доступа.
7. `authenticate_user(username: str, password: str, session: Session)`: Функция для аутентификации пользователя.
8. `get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session))`: Функция для получения текущего пользователя.
9. `read_users_me(current_user: User = Depends(get_current_user))`: Обработчик GET запроса для получения информации о текущем пользователе.

## Вывод
Лабораторная работа по работе с FastAPI позволила освоить разработку веб-приложений с использованием данного фреймворка. В ходе работы были изучены и применены различные концепции, такие как создание роутов, работа с моделями данных, аутентификация и авторизация пользователей, использование базы данных для хранения информации.