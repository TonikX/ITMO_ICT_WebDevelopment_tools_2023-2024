# БД
## Подключение к базе дынных

Было реализована подключение к рабочей базе данныз для хранения информации о пользователях и задачах:

    load_dotenv()
    db_url = os.getenv('DB_ADMIN')
    engine = create_engine(db_url, echo=True)
    
    
    def init_db():
        SQLModel.metadata.create_all(engine)
    
    
    def get_session():
        with Session(engine) as session:
            yield session


# Модели

Были релизованы модели для следующих сущностей:

* `StatusEnum` - статусы задачи;
* `PriorityEnum` - приоритеты задачи;
* `Tag` - тег задачи;
* `Category` - категория задачи;
* `User` - пользователи;
* `TaskTime` - время выполения задачи;
* `Task` - задача;
* `Token` - токен авторизации.

Код реализации:

    from sqlmodel import SQLModel, Field, Relationship
    from typing import Optional, List
    from enum import Enum
    from datetime import date, datetime
    from passlib.context import CryptContext
    
    
    # Enum для приоритета и статуса задач
    class PriorityEnum(str, Enum):
        high = "High"
        medium = "Medium"
        low = "Low"
    
    
    class StatusEnum(str, Enum):
        to_do = "To do"
        in_progress = "In progress"
        done = "Done"
    
    
    # Базовая модель для Category
    class CategoryDefault(SQLModel):
        title: str
        description: Optional[str] = ""
    
    
    # Расширенная модель для Category
    class Category(CategoryDefault, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        tasks: List["Task"] = Relationship(back_populates="category")
    
    
    class TaskTagLink(SQLModel, table=True):
        tag_id: int = Field(foreign_key="tag.id", primary_key=True)
        task_id: int = Field(foreign_key="task.id", primary_key=True)
    
    
    class TagDefault(SQLModel):
        name: str
    
    
    class Tag(TagDefault, table=True):
        id: int = Field(default=None, primary_key=True)
        tasks: List["Task"] = Relationship(back_populates="tags", link_model=TaskTagLink)
    
    
    # Модель для Task
    class TaskDefault(SQLModel):
        title: str
        description: str
        deadline: date
        created_date: date = Field(default_factory=date.today)
        priority: PriorityEnum
        status: StatusEnum
        category_id: Optional[int] = Field(default=None, foreign_key="category.id")
        user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    
    
    class Task(TaskDefault, table=True):
        id: int = Field(default=None, primary_key=True)
        category: Optional[Category] = Relationship(back_populates="tasks")
        tags: List[Tag] = Relationship(back_populates="tasks", link_model=TaskTagLink)
        user: Optional["User"] = Relationship(back_populates="tasks")
        task_time: Optional["TaskTime"] = Relationship(back_populates="task")
    
    
    class TaskResponse(TaskDefault, table=False):
        id: int
        tags: List["Tag"] = []
    
        class Config:
            orm_mode = True
    
    
    # Модель для отслеживания времени выполнения задачи
    class TaskTime(SQLModel, table=True):
        id: int = Field(default=None, primary_key=True)
        start_time: Optional[datetime] = None
        end_time: Optional[datetime] = None
        task_id: Optional[int] = Field(default=None, foreign_key="task.id")
        task: Optional["Task"] = Relationship(back_populates="task_time")
    
    
    # Базовая модель для User
    class UserDefault(SQLModel):
        username: str
        password: Optional[str]
        email: str
        registration_date: date = Field(default_factory=date.today)
    
    
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    
    # Модель пользователя с хэшированием паролей и связью с задачами
    class User(UserDefault, table=True):
        id: int = Field(default=None, primary_key=True)
        hashed_password: str = None
        tasks: List["Task"] = Relationship(back_populates="user")
    
    
    class Token(SQLModel):
        access_token: str
        token_type: str

# Категори
## Эндпоинты для категорий

Были реализованы следующие эндпоинты:
* получение списка категорий;
* получение категории по id;
* добавление категории;
* удаление категории;
* изменение категории.


Код реализации:


    router = APIRouter()
    
    @router.get("/")
    def categories_list(session=Depends(get_session)) -> List[Category]:
        return session.exec(select(Category)).all()
    
    @router.get("/{category_id}")
    def get_category(category_id: int, session=Depends(get_session)) -> Category:
        category = session.get(Category, category_id)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        return category
    
    @router.post("/")
    def category_create(category: CategoryDefault, session=Depends(get_session)) -> TypedDict('Response', {"status": int, "data": Category}):
        category = Category.model_validate(category)
        session.add(category)
        session.commit()
        session.refresh(category)
        return {"status": 200, "data": category}
    
    @router.delete("/{category_id}")
    def delete_category(category_id: int, session=Depends(get_session)) -> TypedDict('Response', {"is_deleted": bool}):
        category = session.get(Category, category_id)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        session.delete(category)
        session.commit()
        return {"is_deleted": True}
    
    @router.patch("/{category_id}")
    def update_category(category_id: int, category: CategoryDefault, session=Depends(get_session)) -> Category:
        db_category = session.get(Category, category_id)
        if not db_category:
            raise HTTPException(status_code=404, detail="Category not found")
        category_data = category.model_dump(exclude_unset=True)
        for key, value in category_data.items():
            setattr(db_category, key, value)
        session.add(db_category)
        session.commit()
        session.refresh(db_category)
        return db_category

# Теги
## Эндпоинты для тегов

Были реализованы следующие эндпоинты:

* получение списка тегов;
* получение тега по id;
* удаление тега;
* изменение тега.


Код реализации:

    from typing import List
    from fastapi import HTTPException, Depends, APIRouter
    from sqlmodel import select
    from typing_extensions import TypedDict
    from models import Tag, TagDefault
    from connection import get_session
    
    router = APIRouter()
    
    @router.get("/")
    def tags_list(session=Depends(get_session)) -> List[Tag]:
        return session.exec(select(Tag)).all()
    
    @router.get("/{tag_id}")
    def get_tag(tag_id: int, session=Depends(get_session)) -> Tag:
        tag = session.get(Tag, tag_id)
        if not tag:
            raise HTTPException(status_code=404, detail="Tag not found")
        return tag
    
    @router.post("/")
    def tag_create(tag: TagDefault, session=Depends(get_session)) -> TypedDict('Response', {"status": int, "data": Tag}):
        tag = Tag.model_validate(tag)
        session.add(tag)
        session.commit()
        session.refresh(tag)
        return {"status": 200, "data": tag}
    
    @router.delete("/{tag_id}")
    def delete_tag(tag_id: int, session=Depends(get_session)) -> TypedDict('Response', {"is_deleted": bool}):
        tag = session.get(Tag, tag_id)
        if not tag:
            raise HTTPException(status_code=404, detail="Tag not found")
        session.delete(tag)
        session.commit()
        return {"is_deleted": True}
    
    @router.patch("/{tag_id}")
    def update_tag(tag_id: int, tag: TagDefault, session=Depends(get_session)) -> Tag:
        db_tag = session.get(Tag, tag_id)
        if not db_tag:
            raise HTTPException(status_code=404, detail="Tag not found")
        tag_data = tag.model_dump(exclude_unset=True)
        for key, value in tag_data.items():
            setattr(db_tag, key, value)
        session.add(db_tag)
        session.commit()
        session.refresh(db_tag)
        return db_tag

# Пользователи
## Эндпоинты для пользователей

    Были реализованы следующие эндпоинты:
    
    * получение списка пользователей;
      * получение пользователя по id;
      * создание пользователя;
      * удаление пользователя;
      * изменение пользователя;
      * получение списка задач для зарегистрированного пользователя;
    
    
    Код реализации:
    
    from datetime import date
    from typing import List, Optional, Type, Sequence
    from fastapi import HTTPException, Depends, APIRouter
    from passlib.context import CryptContext
    from sqlmodel import select, Session
    
    from models import User, UserDefault, Task
    from connection import get_session
    
    router = APIRouter()
    
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    # Получить список всех пользователей
    @router.get("/")
    def get_users(session: Session = Depends(get_session)) -> Sequence[User]:
        return session.exec(select(User)).all()
    
    
    # Получить конкретного пользователя по его ID
    @router.get("/{user_id}", response_model=UserDefault)
    def get_user(user_id: int, session: Session = Depends(get_session)) -> Type[User]:
        user = session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    
    
    # Создать нового пользователя
    @router.post("/", response_model=UserDefault)
    def create_user(user_data: UserDefault, session: Session = Depends(get_session)) -> User:
        hashed_password = pwd_context.hash(user_data.password)
        new_user = User(username=user_data.username, email=user_data.email, hashed_password=hashed_password)
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        return new_user
    
    
    # Обновить информацию о пользователе
    @router.patch("/{user_id}", response_model=UserDefault)
    def update_user(
            user_id: int,
            username: Optional[str] = None,
            email: Optional[str] = None,
            password: Optional[str] = None,
            session: Session = Depends(get_session)
    ) -> Type[User]:
        user = session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
    
        if username:
            user.username = username
        if email:
            user.email = email
        if password:
            user.password = user.hash(password)
    
        session.commit()
        session.refresh(user)
        return user
    
    
    # Удалить пользователя
    @router.delete("/{user_id}")
    def delete_user(user_id: int, session: Session = Depends(get_session)):
        user = session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        session.delete(user)
        session.commit()
        return {"status": "User deleted"}
    
    
# Задачи
## Эндпоинты для задач

Были реализованы следующие эндпоинты:

* получение списка задач;
* получение задачи по id;
* создание задачи;
* удаление задачи;
* изменение задачи;
* добавление тегов задачи;
* начало задачи;
* заверешение задачи;
* пауза задачи;
* получение времени выполнения задачи.


Код реализации:

    from datetime import datetime, date
    from typing import List, Optional
    from fastapi import HTTPException, Depends, APIRouter
    from sqlalchemy.orm import selectinload, joinedload
    from sqlmodel import select, Session
    from typing_extensions import TypedDict
    from models import Task, TaskDefault, TaskTime, StatusEnum, PriorityEnum, TagDefault, Tag, TaskResponse
    from connection import get_session
    
    router = APIRouter()
    
    
    @router.get("/", response_model=List[Task])
    def tasks_list(session=Depends(get_session)) -> List[Task]:
        return session.exec(select(Task)).all()
    
    
    @router.get("/{task_id}", response_model=TaskResponse)
    def get_task(task_id: int, session=Depends(get_session)) -> TaskResponse:
        task = session.exec(select(Task).where(Task.id == task_id).options(joinedload(Task.tags))).first()
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
    
        return TaskResponse.from_orm(task)
    
    
    
    @router.post("/")
    def create_task(
            task_data: TaskDefault,
            tag_data: List[TagDefault] = None,
            session=Depends(get_session)
    ) -> TypedDict('Response', {"status": int, "data": Task, "tag_data": List}):
        # Инициализируем тегов, если их нет
        if tag_data is None:
            tag_data = []
    
        # Создаем объект задачи из предоставленных данных
        task = Task(**task_data.dict())
        session.add(task)
        session.flush()  # Сохраняем задачу, чтобы получить ее ID
    
        # Обработка тегов
        for tag_info in tag_data:
            if tag_info.name:  # Проверяем, что имя тега не пустое
                existing_tag = session.exec(select(Tag).where(Tag.name == tag_info.name)).first()
                if existing_tag:
                    task.tags.append(existing_tag)  # Добавляем существующий тег
                else:
                    new_tag = Tag(**tag_info.dict())
                    session.add(new_tag)
                    session.flush()  # Сохраняем новый тег
                    task.tags.append(new_tag)  # Добавляем новый тег к задаче
    
        session.commit()  # Сохраняем все изменения
        session.refresh(task)  # Обновляем объект задачи с новыми данными
    
        return {"status": 200, "data": task, "tag_data": [tag_info.dict() for tag_info in tag_data]}
    
    
    @router.patch("/{task_id}/add_tags")
    def add_tags_to_task(
            task_id: int,
            tag_data: List[TagDefault],
            session=Depends(get_session)
    ) -> TypedDict('Response', {"message": str}):
        task = session.get(Task, task_id)
    
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
    
        # Обработка тегов
        for tag_info in tag_data:
            if tag_info.name:  # Проверяем, что имя тега не пустое
                existing_tag = session.exec(select(Tag).where(Tag.name == tag_info.name)).first()
                if existing_tag:
                    task.tags.append(existing_tag)  # Добавляем существующий тег
                else:
                    new_tag = Tag(**tag_info.dict())
                    session.add(new_tag)
                    session.flush()  # Сохраняем новый тег
                    task.tags.append(new_tag)  # Добавляем новый тег к задаче
            else:
                raise HTTPException(status_code=400, detail="Tag name cannot be empty")
    
        session.commit()  # Сохраняем изменения
    
        return {"message": "Tags added to task successfully"}
    
    
    @router.patch("/{task_id}/start_task")
    def start_task(task_id: int, session=Depends(get_session)) -> TypedDict('Response', {"message": str}):
        task = session.get(Task, task_id)
    
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
    
        # Если task_time не инициализирован, создайте новый объект TaskTime
        if task.task_time is None:
            task.task_time = TaskTime()  # Инициализация нового объекта TaskTime
    
        task.task_time.start_time = datetime.now()
        task.status = StatusEnum.in_progress
        session.commit()
    
        return {"message": "Task start time and status updated successfully"}
    
    
    @router.patch("/{task_id}/finish_task")
    def finish_task(task_id: int, session=Depends(get_session)) -> TypedDict('Response', {"message": str}):
        task = session.get(Task, task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
    
        task.task_time.end_time = datetime.now()
        task.status = StatusEnum.done
        session.commit()
    
        return {"message": "Task finished successfully"}
    
    
    @router.patch("/{task_id}/time_spent")
    def get_task_time(task_id: int, session=Depends(get_session)) -> TypedDict('Response', {"task_id": int, "total_time_spent": str}):
        task = session.get(Task, task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
    
        # Проверяем, инициализирован ли task_time
        if task.task_time is None or task.task_time.start_time is None or task.task_time.end_time is None:
            raise HTTPException(status_code=400, detail="Task has not been started or finished yet")
    
        # Вычисляем общее время, потраченное на задачу
        total_time_spent = task.task_time.end_time - task.task_time.start_time
    
        return {"task_id": task_id, "total_time_spent": str(total_time_spent)}
    
    
    @router.delete("/{task_id}")
    def delete_task(task_id: int, session=Depends(get_session)) -> TypedDict('Response', {"is_deleted": bool}):
        task = session.get(Task, task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        session.delete(task)
        session.commit()
        return {"is_deleted": True}
    
    
    @router.patch("/{task_id}")
    def update_task(
            task_id: int,
            title: Optional[str] = None,
            description: Optional[str] = None,
            deadline: Optional[date] = None,
            priority: Optional[PriorityEnum] = None,
            category_id: Optional[int] = None,
            session: Session = Depends(get_session)
    ) -> TypedDict('Response', {"title": str, "description": str, "deadline": date, "priority": PriorityEnum,
                                "category_id": Optional[int]}):
        task = session.get(Task, task_id)
    
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
    
        update_data = {
            "title": title,
            "description": description,
            "deadline": deadline,
            "priority": priority,
            "category_id": category_id
        }
    
        for field, value in update_data.items():
            if value is not None:
                setattr(task, field, value)
    
        session.commit()
    
        return {
            "title": task.title,
            "description": task.description,
            "deadline": task.deadline,
            "priority": task.priority,
            "category_id": task.category_id
        }

# Авторизация

Для авторизации были реализованы методы для получения токена 
пользователем. Далее по этому токену возможна реализаци методов 
с авторизированными пользователями.

Код реализации:
    
    from jose import jwt, JWTError
    from passlib.context import CryptContext
    from datetime import datetime, timedelta
    from typing import Any, Union
    from fastapi.security import OAuth2PasswordBearer
    from connection import get_session
    from sqlmodel import select
    
    from fastapi import status
    from fastapi import Depends, HTTPException
    from models import User, Token
    from sqlmodel import Session
    
    SECRET_KEY = "SECRET_KEY"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 60
    
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")
    
    
    def create_access_token(data: dict, expires_delta: timedelta or None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
    
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)
    
    
    def get_current_user_id(token: str) -> int | None:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            sub = payload.get("sub")
            if not sub:
                return None
            user_id = int(sub)
            return user_id
        except jwt.JWTError:
            return None
    
    
    def get_current_user(token: str = Depends(oauth2_scheme),
                               session: Session = Depends(get_session)):
        credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                             detail="Could not validate credentials",
                                             headers={"WWW-Authenticate": "Bearer"})
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise credential_exception
    
        except JWTError:
            raise credential_exception
    
        user = get_user_by_username(username, session=session)
        if user is None:
            raise credential_exception
    
        return user
    
    
    def get_user_by_username(username: str, session=Depends(get_session)) -> Union[User, None]:
        query = select(User).where(User.username == username)
        user = session.exec(query).first()
        return user
    
    
    def get_user_by_id(id: int, session=Depends(get_session)) -> Union[User, None]:
        query = select(User).where(User.id == id)
        user = session.exec(query).first()
        return user
    
    
    def authenticate(username: str, password: str, session=Depends(get_session)) -> Union[User, None]:
        user = get_user_by_username(username, session)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user




Были так же реализованы эндпоинты для регистрации пользователя и получения текущего пользователя.

Код реализации:

    from datetime import timedelta
    from fastapi import APIRouter, status, Depends, HTTPException
    from sqlmodel import Session, select
    from fastapi.security import OAuth2PasswordRequestForm
    from typing import List, Annotated, Sequence
    
    from models import User, Token, Task
    from connection import get_session
    from service.auth import authenticate, create_access_token, get_current_user
    
    router = APIRouter()
    
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    
    
    @router.post("/login", status_code=status.HTTP_202_ACCEPTED, response_model=Token)
    def login_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        session: Session = Depends(get_session)
    ) -> Token:
        # Аутентификация пользователя по его логину и паролю
        user = authenticate(
            username=form_data.username, password=form_data.password, session=session
        )
        if not user:
            raise HTTPException(status_code=400, detail="Incorrect username or password")
    
        # Создание токена доступа
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
    
    
    # Получение данных текущего пользователя
    @router.get("/me", response_model=User)
    async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
        return current_user
    
    
    # Получение задач текущего пользователя
    @router.get("/me/tasks", response_model=List[Task])
    async def get_user_tasks(
        current_user: Annotated[User, Depends(get_current_user)],
        session: Session = Depends(get_session)
    ) -> Sequence[Task]:
        # Проверка существования текущего пользователя
        if not current_user:
            raise HTTPException(status_code=404, detail="User not found")
    
        # Получение задач, связанных с пользователем
        tasks_query = select(Task).where(Task.user_id == current_user.id)
        tasks = session.exec(tasks_query).all()
        return tasks

