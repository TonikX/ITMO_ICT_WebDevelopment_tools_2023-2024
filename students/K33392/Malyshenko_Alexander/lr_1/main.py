from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from models.models import *
from sqlmodel import select
from auth.jwtGenerator import *

from auth import connection as auth
from passlib.context import CryptContext
import bcrypt
from connections.connection import *

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
CRYPT_SALT = os.getenv("CRYPT_SALT")


def getUser(session: Session, username: str) -> User:
    user = session.exec(select(User).where(User.username == username)).first()
    return user


def getUser(session: Session, username: str, hashedPassword: str) -> User:
    user = session.exec(select(User).where(User.username == username,
                                           User.password == hashedPassword)).first()
    return user


def authenticate(session: Session, username: str, hashedPassword: str) -> User:
    user = getUser(session, username, hashedPassword)
    return user


def getPasswordHash(password: str) -> str:
    return bcrypt.hashpw(password.encode(), salt=(CRYPT_SALT).encode()).decode()


def getCurrentUser(token: str = Depends(oauth2_scheme), session=Depends(get_session)):
    decoded_data = verifyJWTToken(token)

    if not decoded_data:
        raise HTTPException(status_code=400, detail="Invalid token")

    user = getUser(session=session, username=decoded_data["sub"], hashedPassword=decoded_data["pas"])
    if not user:
        raise HTTPException(status_code=400, detail="User not found")

    return user


@app.post("/register", response_model=UserDefault)
def userRegister(user: UserDefault, password: str, session=Depends(get_session)) -> UserPassword:
    hashedPassword = getPasswordHash(password=password)
    if authenticate(session, user.username, hashedPassword):
        raise HTTPException(status_code=400, detail="User already exist")

    data = user.__dict__
    data.update({"password": hashedPassword})
    newUser = User(**data)
    session.add(newUser)
    session.commit()
    session.refresh(newUser)
    return newUser


@app.post("/token")
def login(data: OAuth2PasswordRequestForm = Depends(), session=Depends(get_session)) -> dict[str, str]:
    hashedPassword = getPasswordHash(password=data.password)
    user = authenticate(session, data.username, hashedPassword)
    if not user:
        raise HTTPException(status_code=400, detail="No such user register")

    jwt_token = createJWTToken(data={"sub": user.username, "pas": user.password})
    return {"access_token": jwt_token, "token_type": "bearer"}


@app.get("/users/me")
def getUserMe(currentUser: User = Depends(getCurrentUser), session=Depends(get_session)):
    currentUserDict = currentUser.__dict__
    skills = session.exec(select(UserSkill).where(UserSkill.user_id == currentUser.id)).all()
    currentUserDict.update({"skills": skills})

    travels = session.exec(select(Travel, UserTravelLink)
                           .where(UserTravelLink.travel_id == Travel.id,
                                  UserTravelLink.user_id == currentUser.id)).all()
    currentUserDict.update({"travels": travels})
    return currentUserDict


# region skills
@app.post("/users/me/skills/add")
def addUserSkills(description: str, experience: float,
                  currentUser: User = Depends(getCurrentUser), session=Depends(get_session)) -> UserSkill:
    newSkill = UserSkill(user_id=currentUser.id, description=description, experience=experience)
    session.add(newSkill)
    session.commit()
    session.refresh(newSkill)
    return newSkill


@app.put("/users/me/skills/{skill_id/edit")
def editUserSkill(skill_id: int, experience: float, currentUser: User = Depends(getCurrentUser),
                  session=Depends(get_session), description: str = None) -> UserSkill:
    skill: UserSkill = session.get(UserSkill, skill_id)
    if not skill:
        raise HTTPException

    if skill.user_id != currentUser.id:
        raise HTTPException

    if description is not None:
        skill.description = description

    skill.experience = experience
    session.commit()
    session.refresh(skill)
    return skill


@app.delete("/users/me/skills/{skill_id}/delete")
def delUserSkill(skill_id: int, currentUser: User = Depends(getCurrentUser), session=Depends(get_session)) -> dict:
    skill = session.get(UserSkill, skill_id)
    if not skill:
        raise HTTPException

    if skill.user_id != currentUser.id:
        raise HTTPException

    session.delete(skill)
    session.commit()
    return {"msg": "deleted successfully"}
# endregion




@app.on_event("startup")
def on_startup():
    init_db()
