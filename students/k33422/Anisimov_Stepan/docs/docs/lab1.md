# Лабораторная работа №1

В ходе данной лабораторной работы была создана простая система для проведения хакатонов средствами FastAPI и SQLModel.

## Модели

База данных представлена следующими таблицами: 

* Пользователь (User)
* Команда (Team)
* Соревнование (Competition)
* Задача (Task)
* Проект (Project)

```
#user-team link
class UserTeamLink(SQLModel, table=True):
    team_id: int = Field(foreign_key="team.id", primary_key=True)
    user_id: int = Field(foreign_key="user.id", primary_key=True)
```
Модель UserTeamLink предназначена для реализации связи Many-to-Many между участниками соревнований и командами. 
В нее входит 2 поля - первичных ключа. Один из них относится к участнику, второй - к команде.
```
#user
class User(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    teams: Optional[List["Team"]] = Relationship(back_populates="members", link_model=UserTeamLink)
```
Модель User описывает пользователя - участника соревнований. Он описывается id, именем и списком команд, членом которых он является.
```
#team
class TeamDefault(SQLModel):
    name: str

class Team(TeamDefault, table=True):
    id: int = Field(primary_key=True)
    members: List["User"] = Relationship(back_populates="teams", link_model=UserTeamLink)
    projects: Optional[List["Project"]] = Relationship(back_populates="team")

class TeamResponse(TeamDefault):
    id: int
    members: List["User"] = []
    projects: List["Project"] = []
```
Подобный синтаксис для модели Team предназначен для реализации вложенного отображения полей. Так, в соответствующую модель Default входят только поля, вносимые при отправке POST-запроса, а в модель Response - поля, отображаемые при отправке связанного с моделью GET-запроса.
```
#competition
class CompetitionDefault(SQLModel):
    name: str
    description: str

class Competition(CompetitionDefault, table=True):
    id: int = Field(primary_key=True)
    tasks: Optional[List["Task"]] = Relationship(back_populates="comp")

class CompetitionResponse(CompetitionDefault):
    id: int
    tasks: List["Task"] = []
```
Аналогичным образом устроена модель Competition, в ней реализовано вложенное отображение задач, поставленных на том или ином хакатоне.
```
#task 
class TaskDefault(SQLModel):
    name: str
    description: str
    deadline: datetime
    comp_id: int = Field(foreign_key="competition.id")


class Task(TaskDefault, table=True):
    id: int = Field(primary_key=True)
    comp: Competition = Relationship(back_populates="tasks")
    solutions: Optional[List["Project"]] = Relationship(back_populates="task")


class TaskResponse(TaskDefault):
    id: int
    comp: Competition = None
    solutions: List["Project"] = []
```
Так же и для модели Task, здесь списком отображаются детали о предложенных решениях.
```
# project
class ProjectNomination(Enum):
    first = "first"
    second = "second"
    third = "third"
    participant = "participant"


class ProjectDefault(SQLModel):
    name: str
    description: str
    grade: Optional[int]
    nomination: ProjectNomination
    task_id: int = Field(foreign_key="task.id")
    team_id: int = Field(foreign_key="team.id")


class Project(ProjectDefault, table=True):
    id: int = Field(primary_key=True)
    task: Task = Relationship(back_populates="solutions")
    team: Team = Relationship(back_populates="projects")


class ProjectResponse(ProjectDefault):
    id: int
    task: Task = None
    team: Team = None
```
В модели проекта используется поле типа Enum для назначения номинации тому или иному проекту.

## Подключение к базе данных

```
load_dotenv()
db_url = os.getenv('DB_ADMIN')
engine = create_engine(db_url, echo=True)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
```
В качестве СУБД используется PostgreSQL, связь с ней осуществляется при помощи драйвера psycopg2. 
Из файла .env подгружается переменная окружения с адресом базы данных, SQLModel создает описанные в models.py таблицы, и в конце определяется функция для создания сеанса связи с базой данных.

## Запросы к базе данных

Для всех моделей реализованы типовые запросы (GET, POST, PATCH и DELETE), идентичные для каждой из них.
Параметр response_model в декораторе отвечает за валидацию возвращаемых данных.
Функции передается объект Depends, который не позволяет послать запрос до установления сеанса соединения с базой данных.
Рассмотрим запросы на примере модели Team.
```
# team-related CRUDs
@app.post('/team/', response_model=Team)
def create_team(team: Team, session=Depends(get_session)):
    session.add(team)
    session.commit()
    session.refresh(team)
    return team
```
POST-запрос вносит в базу данных информацию о команде. При этом на вход подается только ее название. Id генерируется автоматически, списки участников и проектов подгружаются благодаря информации из других таблиц.
```
@app.get('/teams', response_model=List[Team])
def teams_list(session=Depends(get_session)):
    teams = session.exec(select(Team)).all()
    return teams
```
Первый GET-запрос выводит список всех команд, возвращая данные в соответствующем формате. Функция select из SQLAlchemy соответствует необходимому нам SQL-запросу.
```
@app.get('/teams/{team_id}', response_model=TeamResponse)
def get_team(team_id: int, session=Depends(get_session)):
    team = session.get(Team, team_id)
    return team
```
Второй GET-запрос возвращает команду по ее id и использует созданную специально для вложенного отображения модель TeamResponse. Она предотвращает бесконечную рекурсию при вложенном отображении.
```
@app.patch('/teams/{team_id}', response_model=Team)
def edit_team(team_id: int, team: Team, session=Depends(get_session)):
    existing_team = session.get(Team, team_id)
    if not existing_team:
        raise HTTPException(status_code=404, detail="Team not found")
    team_data = team.model_dump(exclude_unset=True)
    for key, value in team_data.items():
        setattr(existing_team, key, value)
    session.add(existing_team)
    session.commit()
    session.refresh(existing_team)
    return existing_team
```
PATCH-запрос предназначен для частичного обновления данных. Он собирает из базы данные о команде по ее id, затем для каждого поля модели обновляет их в соответствие с запросом пользователя.
```
@app.delete('/teams/{team_id}')
def delete_team(team_id: int, session=Depends(get_session)):
    team = session.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    session.delete(team)
    session.commit()
    return {"ok": True}
```
DELETE-запрос, очевидно, удаляет данные о команде, сначала получая данные о ней, затем стирая из базы данных.

Все изменения в базе данных реализованы при помощи объекта сеанса связи с базой данных, предоставленного SQLModel.

Далее можно увидеть код остальных запросов к базе, реализованных абсолютно идентичными методами.
```
# competition-related CRUDs
@app.post('/competition/', response_model=Competition)
def create_comp(comp: Competition, session=Depends(get_session)):
    session.add(comp)
    session.commit()
    session.refresh(comp)
    return comp


@app.get('/competitions', response_model=List[Competition])
def comps_list(session=Depends(get_session)):
    comps = session.exec(select(Competition)).all()
    return comps


@app.get('/competitions/{competition_id}', response_model=CompetitionResponse)
def get_comp(competition_id: int, session=Depends(get_session)):
    comp = session.get(Competition, competition_id)
    return comp


@app.patch('/competitions/{competition_id}', response_model=Competition)
def edit_comp(comp_id: int, comp: Competition, session=Depends(get_session)):
    existing_comp = session.get(Competition, comp_id)
    if not existing_comp:
        raise HTTPException(status_code=404, detail="Competition not found")
    comp_data = comp.model_dump(exclude_unset=True)
    for key, value in comp_data.items():
        setattr(existing_comp, key, value)
    session.add(existing_comp)
    session.commit()
    session.refresh(existing_comp)
    return existing_comp


@app.delete('/competitions/{competition_id}')
def delete_comp(comp_id: int, session=Depends(get_session)):
    comp = session.get(Competition, comp_id)
    if not comp:
        raise HTTPException(status_code=404, detail="Team not found")
    session.delete(comp)
    session.commit()
    return {"ok": True}


# task-related CRUDs
@app.post('/task/', response_model=Task)
def create_task(task: Task, session=Depends(get_session)):
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@app.get('/tasks', response_model=List[Task])
def tasks_list(session=Depends(get_session)):
    tasks = session.exec(select(Task)).all()
    return tasks


@app.get('/tasks/{task_id}', response_model=TaskResponse)
def get_task(task_id: int, session=Depends(get_session)):
    task = session.get(Task, task_id)
    return task


@app.patch('/tasks/{task_id}', response_model=Task)
def edit_task(task_id: int, task: Task, session=Depends(get_session)):
    existing_task = session.get(Task, task_id)
    if not existing_task:
        raise HTTPException(status_code=404, detail="Task not found")
    task_data = task.model_dump(exclude_unset=True)
    for key, value in task_data.items():
        setattr(existing_task, key, value)
    session.add(existing_task)
    session.commit()
    session.refresh(existing_task)
    return existing_task


@app.delete('/tasks/{task_id}')
def delete_task(task_id: int, session=Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    session.delete(task)
    session.commit()
    return {"ok": True}


# project-related CRUDs
@app.post('/project/', response_model=Project)
def create_project(project: Project, session=Depends(get_session)):
    session.add(project)
    session.commit()
    session.refresh(project)
    return project


@app.get('/projects', response_model=List[Project])
def projects_list(session=Depends(get_session)):
    projects = session.exec(select(Project)).all()
    return projects


@app.get('/projects/{project_id}', response_model=ProjectResponse)
def get_project(project_id: int, session=Depends(get_session)):
    project = session.get(Project, project_id)
    return project


@app.patch('/projects/{project_id}', response_model=Project)
def edit_project(project_id: int, project: Project, session=Depends(get_session)):
    existing_project = session.get(Project, project_id)
    if not existing_project:
        raise HTTPException(status_code=404, detail="Project not found")
    project_data = project.model_dump(exclude_unset=True)
    for key, value in project_data.items():
        setattr(existing_project, key, value)
    session.add(existing_project)
    session.commit()
    session.refresh(existing_project)
    return existing_project


@app.delete('/projects/{project_id}')
def delete_project(project_id: int, session=Depends(get_session)):
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    session.delete(project)
    session.commit()
    return {"ok": True}


# user-related CRUDs
@app.post('/user/', response_model=User)
def create_user(user: User, session=Depends(get_session)):
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@app.get('/users', response_model=List[User])
def users_list(session=Depends(get_session)):
    users = session.exec(select(User)).all()
    return users


@app.get('/users/{user_id}', response_model=User)
def get_user(user_id: int, session=Depends(get_session)):
    user = session.get(User, user_id)
    return user


@app.patch('/users/{user_id}', response_model=User)
def edit_user(user_id: int, user: User, session=Depends(get_session)):
    existing_user = session.get(User, user_id)
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")
    user_data = user.model_dump(exclude_unset=True)
    for key, value in user_data.items():
        setattr(existing_user, key, value)
    session.add(existing_user)
    session.commit()
    session.refresh(existing_user)
    return existing_user


@app.delete('/user/{user_id}')
def delete_user(user_id: int, session=Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return {"ok": True}
```

## Миграции

Миграции служат для обновления таблиц в базе данных в соответствии с изменениями в файле models.py. В данном проекте они реализованы при помощи библиотеки alembic и были активно использованы в ходе тестирования и отладки.

## Выводы

Таким образом, в ходе данной работы при помощи библиотек FastAPI и SQLModel был создан быстрый, легковесный и интуитивно понятный бэкенд для системы организации хакатонов. Все запросы протестированы через автоматически сгенерированную документацию в Swagger, а отражение их результатов в базе данных - через клиент pgAdmin.