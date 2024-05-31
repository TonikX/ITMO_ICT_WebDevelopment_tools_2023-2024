from fastapi import APIRouter, HTTPException, Depends
from auth import AuthHandler
from models import *
from connection import get_session
from starlette.responses import JSONResponse
from starlette.status import HTTP_201_CREATED

router = APIRouter(
    prefix="/user",
    tags=["Пользователи"]
)
auth = AuthHandler()


@router.post('/registration')
def register(user: UserRegistration, session=Depends(get_session)):
    users = auth.select_all_users()
    if any(x.username == user.username for x in users):
        raise HTTPException(status_code=400, detail='Username is taken')
    hashed_password = auth.get_password_hash(user.password)
    new_user = User(username=user.username, password=hashed_password, email=user.email, name=user.name)
    session.add(new_user)
    session.commit()

    return JSONResponse(status_code=201, content={"message": "User registered successfully"})


@router.post('/login')
def login(user: UserLogin):
    user_found = auth.find_user(user.username)

    if not user_found:
        raise HTTPException(status_code=401, detail='Invalid username and/or password')
    verified = auth.verify_password(user.password, user_found.password)

    if not verified:
        raise HTTPException(status_code=401, detail='Invalid username and/or password')

    token = auth.encode_token(user_found.username)
    return {'token': token}


@router.get("/change_password")
def change_password(new_password,
                    session=Depends(get_session),
                    user=Depends(auth.get_current_user)):
    new_hashed_password = auth.get_password_hash(new_password)
    session.query(User).filter(User.id == user.id).update({'password': new_hashed_password})
    session.commit()
    return "OK"


@router.get('')
def get_users(session=Depends(get_session), user=Depends(auth.get_current_user)):
    users = []
    for user in session.query(User).all():
        teams = session.query(Team).filter(Team.user_id == user.id).all()
        members = session.query(TeamMember).filter(TeamMember.user_id == user.id).all()
        participants = []
        for participant in session.query(Participant).filter(Participant.user_id == user.id).all():
            new_participant = GetParticipant(
                id=participant.id,
                user_id=participant.user_id,
                contest_id=participant.contest_id,
                name=participant.name,
                email=participant.email,
                phone=participant.phone
            )

            approval = session.query(ParticipantApprovals).filter(
                ParticipantApprovals.participant_id == participant.id,
            ).first()
            if approval:
                new_participant.is_approval = True
            participants.append(new_participant)
        new_user = GetUser(
            id=user.id,
            username=user.username,
            name=user.name,
            teams=teams,
            members=members,
            participants=participants
        )
        users.append(new_user)
    return users


@router.get('/{user_id}')
def get_user(user_id: int, session=Depends(get_session), user=Depends(auth.get_current_user)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Not found")
    teams = session.query(Team).filter(Team.user_id == user_id).all()
    print(teams)
    print(user_id)
    print("TETT")
    members = session.query(TeamMember).filter(TeamMember.user_id == user_id).all()
    participants = []
    for participant in session.query(Participant).filter(Participant.user_id == user_id).all():
        new_participant = GetParticipant(
            id=participant.id,
            user_id=participant.user_id,
            contest_id=participant.contest_id,
            name=participant.name,
            email=participant.email,
            phone=participant.phone
        )

        approval = session.query(ParticipantApprovals).filter(
            ParticipantApprovals.participant_id == participant.id,
        ).first()
        if approval:
            new_participant.is_approval = True
        participants.append(new_participant)
    new_user = GetUser(
        id=user.id,
        username=user.username,
        name=user.name,
        teams=teams,
        members=members,
        participants=participants
    )
    return new_user


@router.patch('')
def edit_team(new_user: EditUser, session=Depends(get_session), user=Depends(auth.get_current_user)):
    user_data = new_user.model_dump(exclude_unset=True)
    for key, value in user_data.items():
        setattr(user, key, value)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user
