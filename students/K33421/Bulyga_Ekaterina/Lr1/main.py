from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import select
from typing_extensions import TypedDict
from models import *
from sqlmodel import SQLModel, Session, create_engine
import os
from dotenv import load_dotenv
import jwt

from auth.auth import UserManager, SECRET_KEY, ALGORITHM

app = FastAPI()
load_dotenv()
db_url = os.getenv('DB_ADMIN')
engine = create_engine(db_url, echo=True)


@app.on_event("startup")
def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


@app.get("/")
def hello():
    return "Hello!"


user_manager = UserManager()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.post("/register/")
def register_user(user: User, session: Session = Depends(get_session)):
    user_manager.create_user(session, user)
    return {"message": "User registered successfully"}


@app.post("/token/")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    session = Session(engine)
    user = user_manager.get_user(session, username=form_data.username)
    if not user or not user_manager.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = user_manager.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    user = user_manager.get_user(session, username)
    if user is None:
        raise credentials_exception
    return user


@app.get("/users/me/")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


@app.get("/users/{username}/", response_model=User)
async def read_user(username: str, current_user: User = Depends(get_current_user),
                    session: Session = Depends(get_session)):
    # Получаем пользователя из базы данных
    user = user_manager.get_user(session, username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user


@app.get("/users/", response_model=List[User])
async def read_users(current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    # Получаем список пользователей из базы данных
    return session.exec(select(User)).all()


@app.put("/users/change_password/")
async def change_password(new_password: str, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    # Обновляем пароль текущего пользователя
    user_manager.change_password(session, current_user.username, new_password)
    return {"message": "Password changed successfully"}


@app.get("/tasks_list")
def tasks_list(session=Depends(get_session), current_user: User = Depends(get_current_user)) -> List[Task]:
    return session.exec(select(Task)).all()


@app.get("/task/{task_id}", response_model=TaskDayNotificationsUser)
def tasks_get(task_id: int, session=Depends(get_session), current_user: User = Depends(get_current_user)) -> Task:
    task = session.get(Task, task_id)
    return task


@app.post("/task")
def tasks_create(task: TaskDefault, session=Depends(get_session),
                 current_user: User = Depends(get_current_user)) -> TypedDict('Response',
                                                                              {"status": int, "data": Task}):
    task = Task.model_validate(task)
    session.add(task)
    session.commit()
    session.refresh(task)
    return {"status": 200, "data": task}


@app.delete("/task/delete{task_id}")
def task_delete(task_id: int, session=Depends(get_session), current_user: User = Depends(get_current_user)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    session.delete(task)
    session.commit()
    return {"ok": True}


@app.patch("/task{task_id}")
def task_update(task_id: int, task: TaskDefault, session=Depends(get_session),
                current_user: User = Depends(get_current_user)) -> Task:
    db_task = session.get(Task, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    task_data = task.model_dump(exclude_unset=True)
    for key, value in task_data.items():
        setattr(db_task, key, value)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


@app.get("/tasks_users_list")
def tasks_users_list(session=Depends(get_session), current_user: User = Depends(get_current_user)) -> List[TaskUser]:
    return session.exec(select(TaskUser)).all()


@app.get("/task_user/{task_id}&{user_id}", response_model=TaskUser)
def tasks_get(task_id: int, user_id: str, session=Depends(get_session), current_user: User = Depends(get_current_user)) -> TaskUser:
    task_user = session.get(TaskUser, (task_id, user_id))
    return task_user


@app.post("/task_user")
def tasks_users_create(task_user: TaskUser, session=Depends(get_session),
                 current_user: User = Depends(get_current_user)) -> TypedDict('Response',
                                                                              {"status": int, "data": TaskUser}):
    task_user = TaskUser.model_validate(task_user)
    session.add(task_user)
    session.commit()
    session.refresh(task_user)
    return {"status": 200, "data": task_user}


@app.get("/timetabledays_list")
def timetabledays_list(session=Depends(get_session), current_user: User = Depends(get_current_user)) -> List[
    TimetableDay]:
    return session.exec(select(TimetableDay)).all()


@app.get("/timetableday/{timetableday_id}", response_model=TimetableDayWeek)
def timetableday_get(timetableday_id: int, session=Depends(get_session),
                     current_user: User = Depends(get_current_user)) -> TimetableDay:
    day = session.get(TimetableDay, timetableday_id)
    return day


@app.post("/timetableday")
def timetableday_create(day: TimetableDayDefault, session=Depends(get_session),
                        current_user: User = Depends(get_current_user)) -> TypedDict('Response', {"status": int,
                                                                                                  "data": TimetableDay}):
    day = TimetableDay.model_validate(day)
    session.add(day)
    session.commit()
    session.refresh(day)
    return {"status": 200, "data": day}


@app.get("/timetableweeks_list")
def timetableweeks_list(session=Depends(get_session), current_user: User = Depends(get_current_user)) -> List[
    TimetableWeek]:
    return session.exec(select(TimetableWeek)).all()


@app.get("/timetableweek/{timetableweek_id}")
def timetableweek_get(timetableweek_id: int, session=Depends(get_session),
                      current_user: User = Depends(get_current_user)) -> TimetableWeek:
    return session.get(TimetableWeek, timetableweek_id)


@app.post("/timetableweek")
def timetableweek_create(week: TimetableWeek, session=Depends(get_session),
                         current_user: User = Depends(get_current_user)) -> TypedDict('Response', {"status": int,
                                                                                                   "data": TimetableWeek}):
    week = TimetableWeek.model_validate(week)
    session.add(week)
    session.commit()
    session.refresh(week)
    return {"status": 200, "data": week}


@app.get("/tasks_notifications_list")
def tasks_notifications_list(session=Depends(get_session), current_user: User = Depends(get_current_user)) -> List[TaskNotification]:
    return session.exec(select(TaskNotification)).all()


@app.get("/task_notification/{task_id}&{notification_id}", response_model=TaskNotification)
def tasks_notifications_get(task_id: int, notification_id: str, session=Depends(get_session), current_user: User = Depends(get_current_user)) -> TaskNotification:
    task_notification = session.get(TaskNotification, (task_id, notification_id))
    return task_notification


@app.post("/task_notification")
def task_notifications_create(task_notification: TaskNotification, session=Depends(get_session),
                 current_user: User = Depends(get_current_user)) -> TypedDict('Response',
                                                                              {"status": int, "data": TaskNotification}):
    task_notification = TaskNotification.model_validate(task_notification)
    session.add(task_notification)
    session.commit()
    session.refresh(task_notification)
    return {"status": 200, "data": task_notification}


@app.get("/notifications_list")
def notifications_list(session=Depends(get_session), current_user: User = Depends(get_current_user)) -> List[
    Notification]:
    return session.exec(select(Notification)).all()


@app.get("/notification/{notification_id}")
def notification_get(notification_id: int, session=Depends(get_session),
                     current_user: User = Depends(get_current_user)) -> Notification:
    return session.get(Notification, notification_id)


@app.post("/notification")
def notification_create(notification: Notification, session=Depends(get_session),
                        current_user: User = Depends(get_current_user)) -> TypedDict('Response',
                                                                                     {"status": int,
                                                                                      "data": Notification}):
    notification = Notification.model_validate(notification)
    session.add(notification)
    session.commit()
    session.refresh(notification)
    return {"status": 200, "data": notification}


@app.get("/comments_list")
def comments_list(session=Depends(get_session), current_user: User = Depends(get_current_user)) -> List[
    Comment]:
    return session.exec(select(Comment)).all()


@app.get("/comment/{comment_id}", response_model=CommentUserTask)
def comment_get(comment_id: int, session=Depends(get_session),
                     current_user: User = Depends(get_current_user)) -> Comment:
    return session.get(Comment, comment_id)


@app.post("/comment")
def comment_create(comment: CommentDefault, session=Depends(get_session),
                        current_user: User = Depends(get_current_user)) -> TypedDict('Response',
                                                                                     {"status": int,
                                                                                      "data": Comment}):
    comment = Comment.model_validate(comment)
    session.add(comment)
    session.commit()
    session.refresh(comment)
    return {"status": 200, "data": comment}
