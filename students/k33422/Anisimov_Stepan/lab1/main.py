from fastapi import FastAPI, Depends, HTTPException
from connection import *
from models import *
from sqlmodel import select

app = FastAPI()

@app.on_event("startup")
def on_startup():
    init_db()


# team-related CRUDs
@app.post('/team/', response_model=Team)
def create_team(team: Team, session=Depends(get_session)):
    session.add(team)
    session.commit()
    session.refresh(team)
    return team


@app.get('/teams', response_model=List[Team])
def teams_list(session=Depends(get_session)):
    teams = session.exec(select(Team)).all()
    return teams


@app.get('/teams/{team_id}', response_model=TeamResponse)
def get_team(team_id: int, session=Depends(get_session)):
    team = session.get(Team, team_id)
    return team


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


@app.delete('/teams/{team_id}')
def delete_team(team_id: int, session=Depends(get_session)):
    team = session.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    session.delete(team)
    session.commit()
    return {"ok": True}


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
