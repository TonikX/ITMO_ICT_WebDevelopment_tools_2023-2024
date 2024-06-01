import datetime
import os
from typing import List

import jwt
import requests
from celery import Celery
from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import Session, create_engine, select
from sqlalchemy.orm import selectinload

import auth
import models
import schemas


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


app = FastAPI()
celery_app = Celery(
    'worker',
    broker='redis://redis:6379/0',
    backend='redis://redis:6379/0'
)


def get_session():
    with Session(engine) as session:
        yield session


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_session)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    user = db.exec(select(models.User).where(models.User.username == username)).first()
    if user is None:
        raise credentials_exception
    return user


def authenticate_user(db: Session, username: str, password: str):
    statement = select(models.User).where(models.User.username == username)
    user = db.exec(statement).first()
    if not user or not auth.verify_password(password, user.password):
        return False
    return user


@celery_app.task(name="main.call_parser_task")
def call_parser_task(url: str = None):
    try:
        response = requests.post("http://parser:8001/parse", params={"url": url})
        response.raise_for_status()
        result = response.json()
        return {"message": "Parsing successful", "result": result}
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/parse/")
def call_parser(url: str = None, db: Session = Depends(get_session), current_user: models.User = Depends(
    get_current_user)):
    try:
        response = requests.post("http://parser:8001/parse", params={"url": url})
        response.raise_for_status()
        result = response.json()
        return {"message": "Parsing successful", "result": result}
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/parse_async/")
def call_parser_async(url: str = None, db: Session = Depends(get_session), current_user: models.User = Depends(
    get_current_user)):
    task = call_parser_task.apply_async(args=[url])
    return {"message": "Task started", "task_id": task.id}


@app.get("/tasks/{task_id}")
def get_task_status(task_id: str):
    task_result = celery_app.AsyncResult(task_id)
    if task_result.state == 'SUCCESS':
        return {"status": task_result.state, "result": task_result.result}
    elif task_result.state == 'FAILURE':
        return {"status": task_result.state, "result": str(task_result.info)}
    else:
        return {"status": task_result.state}


@app.post("/register/", response_model=schemas.UserBase)
def create_user(user: schemas.UserBase, db: Session = Depends(get_session)):
    statement = select(models.User).where(models.User.username == user.username)
    result = db.exec(statement).first()
    if result:
        raise HTTPException(status_code=400, detail="Username already used")
    hashed_password = auth.hash_password(user.password)
    db_user = models.User(username=user.username, email=user.email, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.post("/token/", response_model=schemas.Token)
def login_for_access_token(db: Session = Depends(get_session), form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/", response_model=schemas.UserResponse)
def about_me(current_user: models.User = Depends(get_current_user)):
    return current_user


@app.get("/users/", response_model=List[schemas.UserResponse])
def get_users(db: Session = Depends(get_session), current_user: models.User = Depends(get_current_user)):
    users = db.exec(select(models.User)).all()
    return users


@app.patch("/users/me/change_password/")
def change_password(change_password: schemas.ChangePasswordBody, db: Session = Depends(get_session), current_user: models.User = Depends(get_current_user)):
    if not auth.verify_password(change_password.old_password, current_user.password):
        raise HTTPException(status_code=400, detail="Old password is incorrect")
    current_user.password = auth.hash_password(change_password.new_password)
    db.commit()
    return {"msg": "Password updated"}


@app.get("/participants/", response_model=List[schemas.ParticipantResponse])
def get_users(db: Session = Depends(get_session), current_user: models.User = Depends(get_current_user)):
    users = db.exec(select(models.Participant)).all()
    return users


@app.post("/participants/", response_model=schemas.ParticipantBase)
def create_participant(participant: schemas.ParticipantBase, db: Session = Depends(get_session), current_user: models.User = Depends(get_current_user)):
    db_participant = models.Participant(**participant.dict())
    db.add(db_participant)
    db.commit()
    db.refresh(db_participant)
    return db_participant


@app.post("/teams/", response_model=schemas.TeamBase)
def create_team(team: schemas.TeamBase, db: Session = Depends(get_session), current_user: models.User = Depends(get_current_user)):
    db_team = models.Team(**team.dict())
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team


@app.get("/teams/", response_model=List[models.Team])
def get_teams(db: Session = Depends(get_session), current_user: models.User = Depends(get_current_user)):
    teams = db.exec(select(models.Team).options(selectinload(models.Team.participants))).all()
    return teams


@app.get("/teams/{team_id}/", response_model=schemas.TeamResponse)
def get_team(team_id: int, db: Session = Depends(get_session), current_user: models.User = Depends(get_current_user)):
    team = db.exec(select(models.Team).where(models.Team.id == team_id).options(selectinload(models.Team.participants))).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team


@app.patch("/teams/{team_id}/participants/")
def add_participant_to_team(team_id: int, participant_id: int, db: Session = Depends(get_session), current_user: models.User = Depends(get_current_user)):
    team = db.exec(select(models.Team).where(models.Team.id == team_id)).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    participant = db.exec(select(models.Participant).where(models.Participant.id == participant_id)).first()
    if not participant:
        raise HTTPException(status_code=404, detail="Participant not found")
    participant.team_id = team.id
    db.commit()
    return {"msg": "Participant added to the team"}


@app.get("/teams/{team_id}/participants/", response_model=List[schemas.ParticipantBase])
def get_team_participants(team_id: int, db: Session = Depends(get_session), current_user: models.User = Depends(get_current_user)):
    participants = db.exec(select(models.Participant).where(models.Participant.team_id == team_id)).all()
    return participants


@app.patch("/teams/{team_id}/status/")
def update_team_status(team_id: int, status: schemas.ApproveStatus, db: Session = Depends(get_session), current_user: models.User = Depends(get_current_user)):
    team = db.exec(select(models.Team).where(models.Team.id == team_id)).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    team.approve_status = status
    db.commit()
    return {"msg": "Team status updated"}


@app.post("/hackathons/")
def create_hackathon(hackathon: schemas.HackathonBase, db: Session = Depends(get_session), current_user: models.User = Depends(get_current_user)):
    db_hackathon = models.Hackathon(**hackathon.dict())
    db.add(db_hackathon)
    db.commit()
    db.refresh(db_hackathon)
    return db_hackathon


@app.get("/hackathons/", response_model=List[schemas.HackathonResponse])
def get_hackathons(db: Session = Depends(get_session), current_user: models.User = Depends(get_current_user)):
    hackathons = db.exec(select(models.Hackathon).options(selectinload(models.Hackathon.tasks))).all()
    return hackathons


@app.get("/hackathons/{hackathon_id}/", response_model=schemas.HackathonResponse)
def get_hackathon(hackathon_id: int, db: Session = Depends(get_session), current_user: models.User = Depends(get_current_user)):
    hackathon = db.exec(select(models.Hackathon).where(models.Hackathon.id == hackathon_id).options(selectinload(models.Hackathon.tasks))).first()
    if not hackathon:
        raise HTTPException(status_code=404, detail="Hackathon not found")
    return hackathon


@app.post("/hackathons/{hackathon_id}/teams/")
def add_team_to_hackathon(hackathon_id: int, team_id: int, db: Session = Depends(get_session), current_user: models.User = Depends(get_current_user)):
    hackathon = db.exec(select(models.Hackathon).where(models.Hackathon.id == hackathon_id)).first()
    if not hackathon:
        raise HTTPException(status_code=404, detail="Hackathon not found")
    team = db.exec(select(models.Team).where(models.Team.id == team_id)).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    db_team_hackathon = models.TeamHackathon(hackathon_id=hackathon.id, team_id=team.id,
                                             registration_date=datetime.datetime.now())
    db.add(db_team_hackathon)
    db.commit()
    return {"msg": "Team added to the hackathon"}


@app.get("/hackathons/{hackathon_id}/teams/", response_model=List[schemas.TeamBase])
def get_hackathon_teams(hackathon_id: int, db: Session = Depends(get_session), current_user: models.User = Depends(get_current_user)):
    teams = db.exec(select(models.Team).join(models.TeamHackathon).where(models.TeamHackathon.hackathon_id == hackathon_id)).all()
    return teams


@app.get("/teams/{team_id}/hackathons/", response_model=List[schemas.HackathonBase])
def get_team_hackathons(team_id: int, db: Session = Depends(get_session), current_user: models.User = Depends(get_current_user)):
    hackathons = db.exec(select(models.Hackathon).join(models.TeamHackathon).where(models.TeamHackathon.team_id == team_id)).all()
    return hackathons


@app.delete("/hackathons/{hackathon_id}/teams/{team_id}/")
def remove_team_from_hackathon(hackathon_id: int, team_id: int, db: Session = Depends(get_session), current_user: models.User = Depends(get_current_user)):
    team_hackathon = db.exec(select(models.TeamHackathon).where(models.TeamHackathon.hackathon_id == hackathon_id,
                                                               models.TeamHackathon.team_id == team_id)).first()
    if not team_hackathon:
        raise HTTPException(status_code=404, detail="Team not found in the hackathon")
    db.delete(team_hackathon)
    db.commit()
    return {"msg": "Team removed from the hackathon"}


@app.post("/hackathons/{hackathon_id}/tasks/")
def create_task(hackathon_id: int, task: schemas.TaskBase, db: Session = Depends(get_session), current_user: models.User = Depends(get_current_user)):
    db_task = models.Task(**task.dict(), hackathon_id=hackathon_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


@app.get("/hackathons/{hackathon_id}/tasks/", response_model=List[schemas.TaskBase])
def get_hackathon_tasks(hackathon_id: int, db: Session = Depends(get_session), current_user: models.User = Depends(get_current_user)):
    tasks = db.exec(select(models.Task).where(models.Task.hackathon_id == hackathon_id)).all()
    return tasks


@app.put("/hackathons/{hackathon_id}/tasks/{task_id}/")
def update_task(hackathon_id: int, task_id: int, task: schemas.TaskBase, db: Session = Depends(get_session), current_user: models.User = Depends(get_current_user)):
    db_task = db.exec(select(models.Task).where(models.Task.id == task_id, models.Task.hackathon_id == hackathon_id)).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    for key, value in task.dict().items():
        setattr(db_task, key, value)
    db.commit()
    db.refresh(db_task)
    return db_task


@app.delete("/hackathons/{hackathon_id}/tasks/{task_id}/")
def delete_task(hackathon_id: int, task_id: int, db: Session = Depends(get_session), current_user: models.User = Depends(get_current_user)):
    db_task = db.exec(select(models.Task).where(models.Task.id == task_id, models.Task.hackathon_id == hackathon_id)).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(db_task)
    db.commit()
    return {"msg": "Task deleted"}


@app.post("/teams/{team_id}/tasks/{task_id}/submissions/")
def create_submission(hackathon_id: int, team_id: int, task_id: int, submission: schemas.SubmissionBase, db: Session = Depends(get_session), current_user: models.User = Depends(get_current_user)):
    db_submission = models.Submission(**submission.dict(), hackathon_id=hackathon_id, team_id=team_id, task_id=task_id)
    db.add(db_submission)
    db.commit()
    db.refresh(db_submission)
    return db_submission


@app.get("/teams/{team_id}/tasks/{task_id}/submissions/", response_model=List[schemas.SubmissionBase])
def get_team_submissions(hackathon_id: int, team_id: int, task_id: int, db: Session = Depends(get_session), current_user: models.User = Depends(get_current_user)):
    submissions = db.exec(select(models.Submission).where(models.Submission.hackathon_id == hackathon_id,
                                                          models.Submission.team_id == team_id,
                                                          models.Submission.task_id == task_id)).all()
    return submissions
