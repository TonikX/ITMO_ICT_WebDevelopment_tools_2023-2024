from fastapi import FastAPI, Depends, HTTPException
import models
from sqlmodel import Session, select
from db import init_db, get_session_depends
import db_queries
from pydantic import ValidationError
import auth
from enum import Enum
import typing as tp
from endpoints import endpoint_tools as tools

app = FastAPI()


class Tags(Enum):
    user = 'user'
    project = 'project'
    category = 'category'
    task = 'task'

@app.on_event("startup")
def on_startup():
    init_db()



# ------------------Token-----------------
@app.post('/token/', status_code=200, tags=[Tags.user])
def create_api_token(
        user_login: models.UserLogin
) -> tp.TypedDict('token_response', {'access_token': str, 'token_type': str}):
    try:
        user_db = db_queries.get_user_by_username(user_login.username)
    except ValueError:
        raise HTTPException(status_code=400, detail=f'no user with username {user_login.username}')

    is_password_correct = auth.verify_password(user_login.password, user_db.hashed_password)
    if not is_password_correct:
        raise HTTPException(status_code=400, detail=f'Incorrect password for username: {user_login.username}')

    token = auth.generate_token(user_login.username)
    return {'access_token': token, 'token_type': 'bearer'}


# ------------------User-------------------

@app.get('/user/{user_id}', status_code=200, tags=[Tags.user])
def get_user_by_id(
        user_id: int,
        session: Session = Depends(get_session_depends)
) -> models.UserGet:
    user = session.get(models.User, user_id)
    if user is None:
        raise HTTPException(
            status_code=404,
            detail=f'user with user_id={user_id} not found'
        )
    user_get = models.UserGet.model_validate(user)
    return user_get


@app.get('/user/', status_code=200, tags=[Tags.user])
def get_current_user(
        user_db:models.User = Depends(auth.get_current_user)
) -> models.UserGet:
    user_get = models.UserGet.model_validate(user_db)
    return user_get

@app.get('/user/list/', status_code=200, tags=[Tags.user])
def get_list_of_users(
    session: Session = Depends(get_session_depends)
)-> tp.List[models.UserGet]:
    query = select(models.User)
    user_db_list = session.exec(query).all()
    user_get_list = [
        models.UserGet.model_validate(user) for user in user_db_list
    ]
    return user_get_list


@app.post('/user/', status_code=201, tags=[Tags.user])
def create_user(
        user: models.UserRegister,
        session:Session=Depends(get_session_depends)
)-> tp.TypedDict('Created message', {'msg': str}):
    hashed_password = auth.get_password_hash(user.password)
    user_data = user.dict()
    user_data['hashed_password'] = hashed_password
    user = models.User.model_validate(user_data)
    tools.add_object_to_db_and_refresh(session, user)
    return {'msg': "Created"}


@app.put('/user/password/', status_code=201, tags=[Tags.user])
def change_user_password(
        user_password: models.UserChangePassword,
        user_db: models.User = Depends(auth.get_current_user),
        session: Session = Depends(get_session_depends)
) -> tp.TypedDict('password_put_response', {'msg': str}):
    is_password_correct = auth.verify_password(user_password.current_password, user_db.hashed_password)
    if not is_password_correct:
        raise HTTPException(status_code=400, detail='Incorrect current password')

    if user_password.new_password != user_password.new_password_verification:
        raise HTTPException(status_code=400, detail='Passwords don\'t match')

    new_hash = auth.get_password_hash(user_password.new_password)
    user_db.hashed_password = new_hash
    session.add(user_db)
    session.commit()
    return {'msg': 'password changed'}




# ------------Project---------------

@app.get('/project/{project_id}', status_code=200, tags=[Tags.project])
def get_project_info(
        project_id: int,
        user_db: models.User = Depends(auth.get_current_user),
        session: Session = Depends(get_session_depends)
) -> models.ProjectBase:
    project_validator = tools.ProjectValidator(session, user_db.id, project_id)
    project_validator.is_in_project_or_exception()
    project = project_validator.object
    project_base = models.ProjectBase.model_validate(project)
    return project_base


@app.get('/project/', status_code=200, tags=[Tags.project])
def get_user_project_list(
    user_db: models.User = Depends(auth.get_current_user),
    session: Session = Depends(get_session_depends)
):
    statement = select(models.ProjectUserLink) \
        .where(models.ProjectUserLink.user_id == user_db.id)
    user_entries: tp.List[models.ProjectUserLink] = list(session.exec(statement).all())
    return [entry.project for entry in user_entries]


@app.post('/project/', status_code=201, tags=[Tags.project])
def create_project(
        project: models.ProjectBase,
        user_db: models.User = Depends(auth.get_current_user),
        session: Session = Depends(get_session_depends)
) -> tp.TypedDict('post_project', {'msg': str}):
    project = models.Project.model_validate(project)
    tools.add_object_to_db_and_refresh(session, project)
    # add creator as project admin
    link = models.ProjectUserLink(
        user_id=user_db.id,
        project_id=project.id,
        role=models.Role.admin
    )
    tools.add_object_to_db_and_refresh(session, link)
    return {'msg': 'Created'}


@app.get('/project/{project_id}/user/', status_code=200, tags=[Tags.project])
def get_list_of_users_in_project(
        project_id: int,
        user_db: models.User = Depends(auth.get_current_user),
        session: Session = Depends(get_session_depends)
) -> tp.List[models.UserGet]:
    project_validator = tools.ProjectValidator(session, user_db.id, project_id)
    project_validator.is_in_project_or_exception()
    project = project_validator.object
    users = project.users
    users_get = [models.UserGet.model_validate(user) for user in users]
    return users_get


@app.post('/project/{project_id}/user/', status_code=200, tags=[Tags.project])
def add_user_to_project(
        project_id: int,
        user_in_project: models.UserInProjectForm,
        session: Session = Depends(get_session_depends),
        user_db: models.User = Depends(auth.get_current_user)
) -> tp.TypedDict('add_to_project', {'msg': str}):
    project_validator = tools.ProjectValidator(session, user_db.id, project_id)
    project_validator.is_admin_or_exception()
    data_for_link = user_in_project.dict()
    data_for_link['project_id'] = project_id
    link = models.ProjectUserLink.validate(data_for_link)
    tools.add_object_to_db_and_refresh(session, link)
    return {'msg': 'Created'}


@app.get('/project/{project_id}/category/', status_code=200, tags=[Tags.project])
def get_project_categories(
        project_id: int,
        session: Session = Depends(get_session_depends),
        user_db: models.User = Depends(auth.get_current_user)
) -> tp.List[models.Category]:
    project_validator = tools.ProjectValidator(session, user_db.id, project_id)
    project_validator.is_in_project_or_exception()
    project = project_validator.object
    return project.categories


@app.post('/project/{project_id}/category/', status_code=201, tags=[Tags.project])
def add_category_to_project(
        project_id: int,
        category: models.CategoryBase,
        session: Session = Depends(get_session_depends),
        user_db: models.User = Depends(auth.get_current_user)
) -> tp.TypedDict('add_category', {'msg': str, 'object': models.Category}):
    project_validator = tools.ProjectValidator(session, user_db.id, project_id)
    project_validator.is_admin_or_exception()
    category = category.dict()
    category['project_id'] = project_id
    category = models.Category.model_validate(category)
    tools.add_object_to_db_and_refresh(session, category)
    return {'msg': 'Created', 'object': category}


@app.get('/project/{project_id}/task', status_code=200, tags=[Tags.project])
def get_project_tasks(
        project_id: int,
        session: Session = Depends(get_session_depends),
        user_db: models.User = Depends(auth.get_current_user)
) -> tp.List[models.CategoryWithBaseTasks]:
    project_validator = tools.ProjectValidator(session, user_db.id, project_id)
    project_validator.is_in_project_or_exception()
    project = project_validator.object
    return project.categories


@app.get('/project/{project_id}/calendar_entries', status_code=200, tags=[Tags.project])
def get_project_calendar_entries(
    project_id: int,
    session: Session = Depends(get_session_depends),
    user_db: models.User = Depends(auth.get_current_user)
) -> models.ProjectWithCalendarEntries:
    project_validator = tools.ProjectValidator(session, user_db.id, project_id)
    project = project_validator.object
    project_validator.is_in_project_or_exception()
    project_with_entries = models.ProjectWithCalendarEntries.model_validate(project)
    return project_with_entries




# -------------------Category---------------
@app.get('/category/{category_id}/', status_code=200, tags=[Tags.category])
def get_category_info(
    category_id: int,
    session: Session = Depends(get_session_depends),
    user_db: models.User = Depends(auth.get_current_user)
) -> models.CategoryBase:
    category_validator = tools.CategoryValidator(session, user_db.id, category_id)
    category = category_validator.object
    category_validator.is_in_project_or_exception()
    category_base = models.CategoryBase.model_validate(category)
    return category_base


@app.get('/category/{category_id}/task/', status_code=200, tags=[Tags.category])
def get_category_tasks(
        category_id: int,
        session: Session = Depends(get_session_depends),
        user_db: models.User = Depends(auth.get_current_user)
):
    category_validator = tools.CategoryValidator(session, user_db.id, category_id)
    category = category_validator.object
    category_validator.is_in_project_or_exception()
    category_with_tasks = models.CategoryWithBaseTasks.model_validate(category)
    return category_with_tasks



@app.post('/category/{category_id}/task/', status_code=201, tags=[Tags.category])
def add_task_to_category(
        category_id: int,
        task: models.TaskBase,
        session: Session = Depends(get_session_depends),
        user_db: models.User = Depends(auth.get_current_user)
) -> tp.TypedDict('task added', {'msg': str, 'obj': models.Task}):
    category_validator = tools.CategoryValidator(session, user_db.id, category_id)
    category_validator.is_admin_or_exception()

    task_data = task.dict()
    task_data['category_id'] = category_id
    task = models.Task.model_validate(task_data)
    tools.add_object_to_db_and_refresh(session, task)
    return {'msg': 'Created', 'obj': task}


@app.get('/category/{category_id}/calendar_entries', status_code=200, tags=[Tags.category])
def get_category_calendar_entries(
        category_id: int,
        session: Session = Depends(get_session_depends),
        user_db: models.User = Depends(auth.get_current_user)
) -> models.CategoryWithEntries:
    category_validator = tools.CategoryValidator(session, user_db.id, category_id)
    category_validator.is_in_project_or_exception()
    category = category_validator.object
    category_with_entries = models.CategoryWithEntries.model_validate(
        category
    )
    return category_with_entries




# ----------------------------Tasks-----------------------------




@app.get('/task/{task_id}', status_code=200, tags=[Tags.task])
def get_task_info(
        task_id: int,
        session: Session = Depends(get_session_depends),
        user_db: models.User = Depends(auth.get_current_user)
) -> models.TaskBase:
    task_validator = tools.TaskValidator(session, user_db.id, task_id)
    task = task_validator.object
    task_validator.is_in_project_or_exception()
    task_base = models.TaskBase.model_validate(task)
    return task_base


@app.post('/task/{task_id}/calendar_entries/', status_code=201, tags=[Tags.task])
def add_calendar_entry_to_task(
        task_id: int,
        calendar_entry: models.CalendarEntryBase,
        session: Session = Depends(get_session_depends),
        user_db: models.User = Depends(auth.get_current_user)
) -> tp.TypedDict('task added', {'msg': str, 'obj': models.CalendarEntry}):
    task_validator = tools.TaskValidator(session, user_db.id, task_id)
    task_validator.is_admin_or_exception()
    calendar_entry_data = calendar_entry.dict()
    calendar_entry_data['task_id'] = task_id
    calendar_entry = models.CalendarEntry.model_validate(calendar_entry_data)
    tools.add_object_to_db_and_refresh(session, calendar_entry)
    return {'msg': 'Created', 'obj': calendar_entry}


@app.get('/task/{task_id}/calendar_entries/', status_code=200, tags=[Tags.task])
def get_task_calendar_entries(
        task_id: int,
        session: Session = Depends(get_session_depends),
        user_db: models.User = Depends(auth.get_current_user)
) -> models.TaskWithEntries:
    task_validator = tools.TaskValidator(session, user_db.id, task_id)
    task = task_validator.object
    task_validator.is_in_project_or_exception()
    task_with_entries = models.TaskWithEntries.model_validate(task)
    return task_with_entries

# def get_task_spent_time(
#         task_id: int,
#         session: Session = Depends(get_session_depends),
#         user_db: models.User = Depends(auth.get_current_user)
# ) -> tp.TypedDict('Task time spent', {'time_spent': int}):
#     task_validator = tools.TaskValidator(session, user_db.id, task_id)
#     task = task_validator.object
#     task_validator.is_in_project_or_exception()
#     task.calend
