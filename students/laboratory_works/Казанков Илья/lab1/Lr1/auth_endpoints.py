from models import UserBase, User, UserShow, ChangePassword
from sqlmodel import select


auth_router = APIRouter()


@auth_router.post('/registration', status_code=201, description='Register new user')
def register(user: UserBase, session=Depends(get_session)):
    users = session.exec(select(User)).all()
def register(user: UserBase, session=Depends(get_session)):
    session.commit()
    return {"status": 201, "message": "Created"}


@auth_router.post('/login')
def login(user: UserBase, session=Depends(get_session)):
    user_found = session.exec(select(User).where(User.username == user.username)).first()
def login(user: UserBase, session=Depends(get_session)):
    token = encode_token(user_found.username)
    return {'token': token}


@auth_router.get('/me', response_model=UserShow)
def get_current_user(user: User = Depends(get_current_user)) -> User:
    return user


@auth_router.patch("/me/change-password")
def user_pwd(user_pwd: ChangePassword, session=Depends(get_session), current=Depends(get_current_user)):
    found_user = session.get(User, current.id)