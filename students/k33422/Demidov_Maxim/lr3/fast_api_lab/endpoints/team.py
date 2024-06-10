from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from typing import List

from pydantic import BaseModel
from sqlmodel import select

from db import get_session
from lib.models import (User, UserTeam, Team, Project, Task, TeamWithUsers,
                        ProjectDefault, ProjectWithTasksAndTeam, TaskDefault)

team_router = APIRouter()

# ---- TEAMS ----

# Create new team
@team_router.post("/teams", response_model=Team)
def create_team(team: Team, session=Depends(get_session)):
    session.add(team)
    session.commit()
    session.refresh(team)
    return team


@team_router.get("/teams", response_model=List[Team])
def get_all_teams(session=Depends(get_session)):
    teams = session.query(Team).all()
    return teams


# Get team by id with information about all users
@team_router.get("/teams/{team_id}", response_model=TeamWithUsers)
def get_team_by_id(team_id: int, session=Depends(get_session)):
    team = session.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team


class AddUserToTeamRequest(BaseModel):
    position: str


# Add user (by id) to team
@team_router.post("/teams/{team_id}/users/{user_id}")
def add_user_to_team(team_id: int, user_id: int, request_body: AddUserToTeamRequest, session=Depends(get_session)):
    team = session.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")

    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    try:

        user_team = UserTeam(user_id=user.id, team_id=team.id, position=request_body.position)

        session.add(user_team)
        session.commit()
    except Exception as e:
        return {"message": "User already in team"}
    return {"message": "User added to team successfully"}


# Delete user from team
@team_router.delete("/teams/{team_id}/users/{user_id}")
def delete_user_from_team(team_id: int, user_id: int, session=Depends(get_session)):
    team = session.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")

    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    try:
        team.users.remove(user)
        session.commit()
    except Exception as e:
        return {"message": "User not in team"}
    return {"message": "User removed from team successfully"}


# Delete team
@team_router.delete("/teams/{team_id}")
def delete_team(team_id: int, session=Depends(get_session)):
    team = session.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")

    session.delete(team)
    session.commit()
    return {"message": "Team deleted successfully"}


# ---- PROJECTS ----
# Create project

@team_router.post("/projects/", response_model=Project)
def create_project(project_data: ProjectDefault, team_id: int, session=Depends(get_session)):
    team = session.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    project = Project(team_id=team_id, **project_data.dict())
    session.add(project)
    session.commit()
    session.refresh(project)
    return project


# Get list of projects
@team_router.get("/projects/", response_model=List[Project])
def get_projects(session=Depends(get_session)):
    return session.query(Project).all()


# Get project with task list by id
@team_router.get("/projects/{project_id}/", response_model=ProjectWithTasksAndTeam)
def get_project_with_tasks(project_id: int, session=Depends(get_session)):
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


# Get list of projects of certain team by id
@team_router.get("/teams/{team_id}/projects/", response_model=List[Project])
def get_projects_by_team_id(team_id: int, session=Depends(get_session)):
    return session.exec(select(Project).where(Project.team_id == team_id)).all()


# Update project information
@team_router.put("/projects/{project_id}/", response_model=Project)
def update_project(project_id: int, project_data: ProjectDefault, session=Depends(get_session)):
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    for field, value in project_data.dict(exclude_unset=True).items():
        setattr(project, field, value)

    session.commit()
    session.refresh(project)
    return project


# Delete project
@team_router.delete("/projects/{project_id}/")
def delete_project(project_id: int, session=Depends(get_session)):
    project = session.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    session.delete(project)
    session.commit()
    return {"message": "Project deleted successfully"}


# ---- TASKS ----
# Create task
@team_router.post("/tasks/", response_model=Task)  # /tasks/?project_id=value
def create_task(task_data: TaskDefault, project_id: int, session=Depends(get_session)):
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    task = Task(project_id=project_id, **task_data.dict())
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


# List all tasks
@team_router.get("/tasks/", response_model=List[Task])
def list_all_tasks(session=Depends(get_session)):
    return session.query(Task).all()


# List all tasks of certain project
@team_router.get("/projects/{project_id}/tasks/", response_model=List[Task])
def list_tasks_by_project(project_id: int, session=Depends(get_session)):
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return session.exec(select(Task).where(Task.project_id == project_id)).all()


# Get certain task by id
@team_router.get("/tasks/{task_id}/", response_model=Task)
def get_task_by_id(task_id: int, session=Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


# Update task by id
@team_router.put("/tasks/{task_id}/", response_model=Task)
def update_task(task_id: int, task_data: Task, session=Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    for field, value in task_data.dict(exclude_unset=True).items():
        setattr(task, field, value)

    session.commit()
    session.refresh(task)
    return task


# List all tasks with missed deadlines
@team_router.get("/tasks/urgent/", response_model=List[Task])
def get_urgent_tasks(session=Depends(get_session)):
    urgent_tasks = session.exec(select(Task).where(Task.deadline < datetime.now())).all()
    return urgent_tasks


# Delete task by id
@team_router.delete("/tasks/{task_id}/")
def delete_task(task_id: int, session=Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    session.delete(task)
    session.commit()
    return {"message": "Task deleted successfully"}
