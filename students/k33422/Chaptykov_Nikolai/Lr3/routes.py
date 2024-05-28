from fastapi import FastAPI, Depends, HTTPException, APIRouter
from sqlmodel import select 
from models import *
from passlib.context import CryptContext
from typing_extensions import TypedDict
from connection import *
import datetime
import jwt
import logging
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select, exc, insert, delete, update


logger = logging.getLogger(__name__)


SECRET_KEY = "iloveyou"
ALGORITHM = "HS256"


router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        return payload['sub']
    except Exception:
        return None


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/token")


@router.get("/me")
async def get_users(token, session=Depends(get_session)):
    temp = decode_token(token)
    if temp:
        user = session.scalars(select(User).where(User.email == temp)).one()
        return {"name": user.email}
    raise HTTPException(status_code=403, detail="Forbidden")


@router.get("/users")
async def get_users(token, session=Depends(get_session)):
    temp = decode_token(token)
    if temp:
        result = session.scalars(select(User)).all()
        return result
    raise HTTPException(status_code=403, detail="Forbidden")


@router.get("/tasks")
async def get_tasks(token, board_id: int = None, session=Depends(get_session)):
    temp = decode_token(token)
    if temp: # проверка валиден ли токен
        user = session.scalars(select(User).where(User.email == temp)).one() # получаем юзера по почте, ассоциированной с токеном
        cmd = select(UsersBoardsLink).where(UsersBoardsLink.board_id == board_id, UsersBoardsLink.user_id == user.id) # проверяем есть ли доступ у пользователя к борду
        if session.scalars(cmd).all():
            cmd_long = select(LongTasks).join(LongBoard).join(Board).filter(LongBoard.board_id == board_id)
            cmd_per = select(PeriodicTasks).join(ShortBoard).join(Board).filter(ShortBoard.board_id == board_id)
            return session.scalars(cmd_per).all(), session.scalars(cmd_long).all()
    raise HTTPException(status_code=403, detail="Forbidden")


@router.get("/tasks/longtasks")
async def get_long(token, board_id: int = None, session=Depends(get_session)):
    temp = decode_token(token)
    if temp:
        user = session.scalars(select(User).where(User.email == temp)).one()
        cmd = select(UsersBoardsLink).where(UsersBoardsLink.board_id == board_id, UsersBoardsLink.user_id == user.id)
        if session.scalars(cmd).all():
            cmd_long = select(LongTasks).join(LongBoard).join(Board).filter(LongBoard.board_id == board_id)
            return session.scalars(cmd_long).all()
    raise HTTPException(status_code=403, detail="Forbidden")


@router.get("/tasks/periodictasks")
async def get_periodic(token, board_id: int = None, session=Depends(get_session)):
    temp = decode_token(token)
    if temp:
        user = session.scalars(select(User).where(User.email == temp)).one()
        cmd = select(UsersBoardsLink).where(UsersBoardsLink.board_id == board_id, UsersBoardsLink.user_id == user.id)
        if session.scalars(cmd).all():
            cmd_per = select(PeriodicTasks).join(ShortBoard).join(Board).filter(ShortBoard.board_id == board_id)
            return session.scalars(cmd_per).all()
    raise HTTPException(status_code=403, detail="Forbidden")


@router.post("/signup")
async def sign_up(user: User, session=Depends(get_session)):
    try:
        user.password = hash_password(user.password)
        session.add(user)
        session.commit()
        return {"message": "success"}
    except exc.IntegrityError:
        return HTTPException(status_code=401, detail="User already exists")


@router.post("/login")
async def login(user: User, session=Depends(get_session)):
    if not session.exec(select(User).where(User.email == user.email)).all():
        raise HTTPException(status_code=401, detail="Invalid email")
    hashed = session.execute(select(User.password).where(User.email == user.email)).first()
    if not verify_password(user.password, hashed.password):
        raise HTTPException(status_code=401, detail="Invalid password")
    access_token = create_access_token({"sub": user.email, "iat": datetime.datetime.utcnow(), "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)})
    return {"access_token": access_token}


@router.post("/create_board")
async def create_board(token: str, session=Depends(get_session)):
    temp = decode_token(token)
    if temp:
        user = session.scalars(select(User).where(User.email == temp)).one()
        board = Board(users=[user], readonly=False)
        session.add(board)
        session.commit()
        user.boards.append(board)
        session.refresh(board)
        session.refresh(user)
        longboard = LongBoard(board_id=board.id)
        shortboard = ShortBoard(board_id=board.id)
        session.add(longboard)
        session.add(shortboard)
        session.commit()
        session.refresh(longboard)
        session.refresh(shortboard)
        return {"message": board}
    raise HTTPException(status_code=403, detail="Forbidden")


@router.delete("/delete_board") # не смог настроить каскадное удаление, поэтому делаю его вручную
async def delete_board(board_id: int, token: str, session=Depends(get_session)):
    temp = decode_token(token)
    if temp:
        user = session.scalars(select(User).where(User.email == temp)).one()
        cmd = select(UsersBoardsLink).where(UsersBoardsLink.board_id == board_id, UsersBoardsLink.user_id == user.id)
        if session.scalars(cmd).all():
            # удаление борд
            delete_longboard = delete(LongBoard).where(LongBoard.board_id == board_id)
            delete_shortboard = delete(ShortBoard).where(ShortBoard.board_id == board_id)
            delete_board = delete(Board).where(Board.id == board_id)
            delete_link = delete(UsersBoardsLink).where(UsersBoardsLink.board_id == board_id)
            # удаление тасков
            cmd_longtasks = select(LongTasks.id).join(LongBoard).where(LongBoard.board_id == board_id)
            cmd_pertasks = select(PeriodicTasks.id).join(ShortBoard).where(ShortBoard.board_id == board_id)
            session.exec(delete(LongTasks).where(LongTasks.id.in_(cmd_longtasks)))
            session.exec(delete(PeriodicTasks).where(PeriodicTasks.id.in_(cmd_pertasks)))
            session.exec(delete_longboard)
            session.exec(delete_shortboard)
            session.exec(delete_link)
            session.exec(delete_board)
            session.commit()
            return {"message": "success"}
    raise HTTPException(status_code=403, detail="Forbidden")


@router.post("/invite_user")
async def invite_user(board_id: int, user_email: str, token: str, readonly: bool = True, session=Depends(get_session)):
    temp = decode_token(token)
    if temp:
        user = session.scalars(select(User).where(User.email == temp)).one()
        cmd = select(UsersBoardsLink).where(UsersBoardsLink.board_id == board_id, UsersBoardsLink.user_id == user.id)
        if session.scalars(cmd).all():
            user_id = session.scalars(select(User.id).where(User.email == user_email)).one()
            link = UsersBoardsLink(user_id=user_id, board_id=board_id, readonly=readonly)
            session.add(link)
            session.commit()
            return {"message": "success"}
    raise HTTPException(status_code=403, detail="Forbidden")


@router.delete("/kick_user")
async def kick_user(board_id: int, user_email: str, token: str, session=Depends(get_session)):
    temp = decode_token(token)
    if temp:
        user = session.scalars(select(User).where(User.email == temp)).one()
        cmd = select(UsersBoardsLink).where(UsersBoardsLink.board_id == board_id, UsersBoardsLink.user_id == user.id)
        if session.scalars(cmd).all():
            user_id = session.scalars(select(User.id).where(User.email == user_email)).one()
            unlink = delete(UsersBoardsLink).where(UsersBoardsLink.user_id == user_id, UsersBoardsLink.board_id == board_id)
            session.exec(unlink)
            session.commit()
            return {"message": "success"}
    raise HTTPException(status_code=403, detail="Forbidden")


@router.post("/create_long")
async def create_long(task: LongTasks, longboard_id: int, token: str, session=Depends(get_session)):
    temp = decode_token(token)
    if temp:
        user = session.scalars(select(User).where(User.email == temp)).one()
        cmd = select(Board).join(LongBoard).join(UsersBoardsLink).where(LongBoard.id == longboard_id, UsersBoardsLink.user_id == user.id, LongBoard.board_id == Board.id, UsersBoardsLink.readonly == False)
        if session.scalars(cmd).all():
            task.longboard_id = longboard_id
            session.add(task)
            session.commit()
            session.refresh(task)
            return {"message": "success"}
    raise HTTPException(status_code=403, detail="Forbidden")


@router.post("/create_periodic")
async def create_periodic(task: PeriodicTasks, shortboard_id: int, token: str, session=Depends(get_session)):
    temp = decode_token(token)
    if temp:
        user = session.scalars(select(User).where(User.email == temp)).one()
        cmd = select(Board).join(ShortBoard).join(UsersBoardsLink).where(ShortBoard.id == shortboard_id, UsersBoardsLink.user_id == user.id, ShortBoard.board_id == Board.id, UsersBoardsLink.readonly == False)
        if session.scalars(cmd).all():
            task.shortboard_id = shortboard_id
            session.add(task)
            session.commit()
            session.refresh(task)
            return {"message": "success"}
    raise HTTPException(status_code=403, detail="Forbidden")


@router.delete("/delete_periodic")
async def delete_periodic(task_id: int, shortboard_id: int, token: str, session=Depends(get_session)):
    temp = decode_token(token)
    if temp:
        user = session.scalars(select(User).where(User.email == temp)).one()
        cmd = select(Board).join(ShortBoard).join(UsersBoardsLink).where(ShortBoard.id == shortboard_id, UsersBoardsLink.user_id == user.id, ShortBoard.board_id == Board.id, UsersBoardsLink.readonly == False)
        if session.scalars(cmd).all():
            delete_task = delete(PeriodicTasks).where(PeriodicTasks.shortboard_id == shortboard_id, PeriodicTasks.id == task_id)
            session.exec(delete_task)
            session.commit()
            return {"message": "success"}
    raise HTTPException(status_code=403, detail="Forbidden")


@router.delete("/delete_long")
async def delete_long(task_id: int, longboard_id: int, token: str, session=Depends(get_session)):
    temp = decode_token(token)
    if temp:
        user = session.scalars(select(User).where(User.email == temp)).one()
        cmd = select(Board).join(LongBoard).join(UsersBoardsLink).where(LongBoard.id == longboard_id, UsersBoardsLink.user_id == user.id, LongBoard.board_id == Board.id, UsersBoardsLink.readonly == False)
        if session.scalars(cmd).all():
            delete_task = delete(LongTasks).where(LongTasks.longboard_id == longboard_id, LongTasks.id == task_id)
            session.exec(delete_task)
            session.commit()
            return {"message": "success"}
    raise HTTPException(status_code=403, detail="Forbidden")


@router.patch("/change_password")
async def change_password(token: str, old_password: str, new_password: str, session=Depends(get_session)):
    temp = decode_token(token)
    if temp:
        user = session.scalars(select(User).where(User.email == temp)).one()
        if not verify_password(old_password, user.password):
            raise HTTPException(status_code=401, detail="Invalid old password")
        user.password = hash_password(new_password)
        session.add(user)
        session.commit()
        return {'message': 'success'}
    raise HTTPException(status_code=403, detail="Forbidden")


@router.post("/add_imgsource")
async def add_imgsource(imgsrc: BaseImageSource, session=Depends(get_session)):
    imgsrc = ImageSource.model_validate(imgsrc)
    cmd = select(ImageSource).where(ImageSource.url == imgsrc.url)
    if db_imgsrc := session.scalars(cmd).first():
        return db_imgsrc
    else:
        session.add(imgsrc)
        session.commit()
        session.refresh(imgsrc)
        return imgsrc


@router.post("/add_img")
async def add_img(img: BaseImage, session=Depends(get_session)):
    img = Image.model_validate(img)
    cmd = select(Image).where(Image.url == img.url)
    if not session.scalars(cmd).first():
        session.add(img)
        session.commit()
        session.refresh(img)
        return img
    raise HTTPException(status_code=409, detail="Row already exists")
