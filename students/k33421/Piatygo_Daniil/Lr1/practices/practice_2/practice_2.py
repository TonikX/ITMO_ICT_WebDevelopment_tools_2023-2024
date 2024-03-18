from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import Session, create_engine, select
from models import Participant, Team, Task, Submission, Hackathon, TeamHackathon
from typing import List


DATABASE_URL = "postgresql://dptgo:iloveweb@localhost:5434/hackathons"
engine = create_engine(DATABASE_URL)

app = FastAPI()


def get_session():
    with Session(engine) as session:
        yield session


@app.post("/participants/", response_model=Participant)
def register_participant(participant: Participant, session: Session = Depends(get_session)):
    db_participant = session.exec(select(Participant).where(Participant.email == participant.email)).first()
    if db_participant:
        raise HTTPException(status_code=400, detail="Email already registered")
    session.add(participant)
    session.commit()
    session.refresh(participant)
    return participant


@app.get("/participants/", response_model=List[Participant])
def list_participants(session: Session = Depends(get_session)):
    participants = session.exec(select(Participant)).all()
    return participants


@app.put("/participants/{participant_id}/", response_model=Participant)
def update_participant(participant_id: int, participant: Participant, session: Session = Depends(get_session)):
    db_participant = session.get(Participant, participant_id)
    if not db_participant:
        raise HTTPException(status_code=404, detail="Participant not found")
    update_data = participant.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_participant, key, value)
    session.add(db_participant)
    session.commit()
    session.refresh(db_participant)
    return db_participant


@app.delete("/participants/{participant_id}/", response_model=Participant)
def delete_participant(participant_id: int, session: Session = Depends(get_session)):
    participant = session.get(Participant, participant_id)
    if not participant:
        raise HTTPException(status_code=404, detail="Participant not found")
    session.delete(participant)
    session.commit()
    return participant


@app.post("/teams/", response_model=Team)
def create_team(team: Team, session: Session = Depends(get_session)):
    session.add(team)
    session.commit()
    session.refresh(team)
    return team


@app.get("/teams/", response_model=List[Team])
def list_teams(session: Session = Depends(get_session)):
    teams = session.exec(select(Team)).all()
    return teams


@app.post("/teams/{team_id}/participants/", response_model=Participant)
def add_participant_to_team(participant_id: int, team_id: int, session: Session = Depends(get_session)):
    participant = session.get(Participant, participant_id)
    if not participant:
        raise HTTPException(status_code=404, detail="Participant not found")
    team = session.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    participant.team_id = team_id
    session.add(participant)
    session.commit()
    session.refresh(participant)
    return participant


@app.delete("/teams/{team_id}/participants/{participant_id}/", response_model=Participant)
def remove_participant_from_team(participant_id: int, team_id: int, session: Session = Depends(get_session)):
    participant = session.get(Participant, participant_id)
    if not participant:
        raise HTTPException(status_code=404, detail="Participant not found")
    if participant.team_id != team_id:
        raise HTTPException(status_code=400, detail="Participant is not in the team")
    participant.team_id = None
    session.add(participant)
    session.commit()
    return participant


@app.get("/teams/{team_id}/participants/", response_model=List[Participant])
def list_team_participants(team_id: int, session: Session = Depends(get_session)):
    participants = session.exec(select(Participant).where(Participant.team_id == team_id)).all()
    return participants


@app.get("/teams/{team_id}/submissions", response_model=List[Submission])
def list_team_submissions(team_id: int, session: Session = Depends(get_session)):
    submissions = session.exec(select(Submission).where(Submission.team_id == team_id)).all()
    return submissions


@app.post("/tasks/", response_model=Task)
def publish_task(task: Task, hackathon_id: int, session: Session = Depends(get_session)):
    hackathon = session.get(Hackathon, hackathon_id)
    if not hackathon:
        raise HTTPException(status_code=404, detail="Hackathon not found")
    task.hackathon_id = hackathon_id
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@app.get("/tasks/", response_model=List[Task])
def list_tasks(hackathon_id: int, session: Session = Depends(get_session)):
    tasks = session.exec(select(Task).where(Task.hackathon_id == hackathon_id)).all()
    return tasks


@app.post("/hackathons/", response_model=Hackathon)
def create_hackathon(hackathon: Hackathon, session: Session = Depends(get_session)):
    session.add(hackathon)
    session.commit()
    session.refresh(hackathon)
    return hackathon


@app.get("/hackathons/", response_model=List[Hackathon])
def list_hackathons(session: Session = Depends(get_session)):
    hackathons = session.exec(select(Hackathon)).all()
    return hackathons


@app.get("/hackathons/{hackathon_id}/", response_model=Hackathon)
def get_hackathon(hackathon_id: int, session: Session = Depends(get_session)):
    hackathon = session.get(Hackathon, hackathon_id)
    if not hackathon:
        raise HTTPException(status_code=404, detail="Hackathon not found")
    return hackathon


@app.get("/hackathons/{hackathon_id}/tasks/", response_model=List[Task])
def list_hackathon_tasks(hackathon_id: int, session: Session = Depends(get_session)):
    tasks = session.exec(select(Task).where(Task.hackathon_id == hackathon_id)).all()
    return tasks


@app.post("/submissions/", response_model=Submission)
def submit_task(submission: Submission, task_id: int, team_id: int, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    team = session.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    submission.task_id = task_id
    submission.team_id = team_id
    session.add(submission)
    session.commit()
    session.refresh(submission)
    return submission


@app.get("/submissions/", response_model=List[Submission])
def list_submissions(session: Session = Depends(get_session)):
    submissions = session.exec(select(Submission)).all()
    return submissions


@app.get("/submissions/{submission_id}/", response_model=Submission)
def get_submission(submission_id: int, session: Session = Depends(get_session)):
    submission = session.get(Submission, submission_id)
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")
    return submission
