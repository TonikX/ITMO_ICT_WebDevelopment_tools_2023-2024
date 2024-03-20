# main.py

```
app = FastAPI(
    title = "Time Managment"
)

@app.on_event("startup")
def on_startup():
    init_db()
    with Session(engine) as session:
            create_data(session)

def create_data(session: Session):
    session.commit()

def main():
    with Session(engine) as session:
        create_data(session)


app.include_router(user_router) 
app.include_router(tasks_router) 
app.include_router(categ_router) 
app.include_router(timelogs_router) 
app.include_router(taskscateg_router) 
app.include_router(add_router) 


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

SECRET_KEY = secrets.token_urlsafe(32)
ALGORITHM = "HS256"

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@app.post("/usersReg")
def create_user(username: str, password: str, session: Session = Depends(get_session)):
    hashed_password = hash_password(password) 
    user = User(username=username, hashed_password=hashed_password)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@app.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    user = authenticate_user(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

def authenticate_user(username: str, password: str, session: Session):
    user = session.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token") 

def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return username
    except JWTError:
        raise credentials_exception

def get_current_active_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    username = verify_token(token, credentials_exception)
    user = session.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user


@app.get("/users/me")
def read_current_user(current_user: User = Depends(get_current_active_user)):
    return current_user

@app.post("/users/change-password")
def change_password(password_change: PasswordChange, current_user: User = Depends(get_current_active_user), session: Session = Depends(get_session)):
    try:
        user = session.query(User).filter(User.id == current_user.id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if not verify_password(password_change.old_password, user.hashed_password):
            raise HTTPException(status_code=400, detail="Incorrect old password")
        user.hashed_password = hash_password(password_change.new_password)
        session.add(user)
        session.commit()
        return {"msg": "Password changed successfully"}
    except SQLAlchemyError as e:
        session.rollback()

        raise HTTPException(status_code=500, detail="Internal Server Error")

```