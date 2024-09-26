from fastapi import FastAPI, Security, HTTPException, Depends
import uvicorn
from models import *
from database import init_db, get_session
from typing_extensions import TypedDict
from datetime import datetime
import datetime
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
import jwt
from starlette import status
from sqlmodel import select


app = FastAPI()


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/parse/")
def cases_list(session=Depends(get_session)) -> list[Site]:
    return session.query(Site).all()

@app.post("/travel/create")
def travel_create(travel: TravelBase, session=Depends(get_session)) \
        -> TypedDict('Response', {"status": int,
                                  "data": Travel}):
    travel = Travel.model_validate(travel)
    session.add(travel)
    session.commit()
    session.refresh(travel)
    return {"status": 200, "data": travel}


@app.get("/travel/list")
def travels_list(session=Depends(get_session)) -> list[Travel]:
    return session.query(Travel).all()


@app.get("/travel/{travel_id}",  response_model=TravelShow)
def travel_get(travel_id: int, session=Depends(get_session)):
    obj = session.get(Travel, travel_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="subtravel not found")
    return obj


@app.patch("/travel/update/{travel_id}")
def travel_update(travel_id: int, travel: TravelBase, session=Depends(get_session)) -> Travel:
    db_travel = session.get(Travel, travel_id)
    if not db_travel:
        raise HTTPException(status_code=404, detail="travel not found")

    travel_data = travel.model_dump(exclude_unset=True)
    for key, value in travel_data.items():
        setattr(db_travel, key, value)
    session.add(db_travel)
    session.commit()
    session.refresh(db_travel)
    return db_travel


@app.delete("/travel/delete/{travel_id}")
def travel_delete(travel_id: int, session=Depends(get_session)):
    travel = session.get(Travel, travel_id)
    if not travel:
        raise HTTPException(status_code=404, detail="travel not found")
    session.delete(travel)
    session.commit()
    return {"ok": True}


@app.post("/companion/create")
def companion_create(companion: CompanionBase, session=Depends(get_session)) \
        -> TypedDict('Response', {"status": int,
                                  "data": Companion}):
    companion = Companion.model_validate(companion)
    session.add(companion)
    session.commit()
    session.refresh(companion)
    return {"status": 200, "data": companion}


@app.get("/companion/list")
def companion_list(session=Depends(get_session)) -> list[Companion]:
    return session.query(Companion).all()


@app.get("/companion/{travel_id}",  response_model=Companion)
def companion_get(travel_id: int, session=Depends(get_session)):
    obj = session.get(Companion, travel_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="travel not found")
    return obj


@app.patch("/companion/update/{companion_id}")
def companion_update(companion_id: int, companion: CompanionBase, session=Depends(get_session)) -> Companion:
    db_travel = session.get(Companion, companion_id)
    if not db_travel:
        raise HTTPException(status_code=404, detail="travel not found")

    companion_data = companion.model_dump(exclude_unset=True)
    for key, value in companion_data.items():
        setattr(db_travel, key, value)
    session.add(db_travel)
    session.commit()
    session.refresh(db_travel)
    return db_travel


@app.delete("/companion/delete/{travel_id}")
def companion_delete(travel_id: int, session=Depends(get_session)):
    travel = session.get(Companion, travel_id)
    if not travel:
        raise HTTPException(status_code=404, detail="travel not found")
    session.delete(travel)
    session.commit()
    return {"ok": True}


@app.post("/region/create")
def region_create(region: RegionBase, session=Depends(get_session)) \
        -> TypedDict('Response', {"status": int,
                                  "data": Region}):
    region = Region.model_validate(region)
    session.add(region)
    session.commit()
    session.refresh(region)
    return {"status": 200, "data": region}


@app.get("/region/list")
def regions_list(session=Depends(get_session)) -> list[Region]:
    return session.query(Region).all()


@app.get("/region/{region_id}",  response_model=Region)
def region_get(region_id: int, session=Depends(get_session)):
    obj = session.get(Region, region_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="Region not found")
    return obj


@app.patch("/region/update/{region_id}")
def region_update(region_id: int, region: RegionBase, session=Depends(get_session)) -> Region:
    db_region = session.get(Region, region_id)
    if not db_region:
        raise HTTPException(status_code=404, detail="Region not found")

    region_data = Region.model_dump(region)
    for key, value in region_data.items():
        setattr(db_region, key, value)
    session.add(db_region)
    session.commit()
    session.refresh(db_region)
    return db_region


@app.delete("/region/delete/{region_id}")
def region_delete(region_id: int, session=Depends(get_session)):
    region = session.get(Region, region_id)
    if not region:
        raise HTTPException(status_code=404, detail="Region not found")
    session.delete(region)
    session.commit()
    return {"ok": True}


@app.post("/whattosee/create")
def whattosee_create(whattosee: WhatToSeeBase, session=Depends(get_session)) \
        -> TypedDict('Response', {"status": int,
                                  "data": WhatToSee}):
    whattosee = WhatToSee.model_validate(whattosee)
    session.add(whattosee)
    session.commit()
    session.refresh(whattosee)
    return {"status": 200, "data": whattosee}


@app.get("/list-whattosees-in-region/{region_id}")
def whattosees_list(region_id: int, session=Depends(get_session)) -> list[WhatToSee]:
    return session.query(WhatToSee).filter(WhatToSee.region_id == region_id).all()


@app.get("/whattosee/{whattosee_id}",  response_model=WhatToSee)
def whattosee_get(whattosee_id: int, session=Depends(get_session)):
    obj = session.get(WhatToSee, whattosee_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="subwhattosee not found")
    return obj


@app.patch("/whattosee/update/{whattosee_id}")
def whattosee_update(whattosee_id: int, whattosee: WhatToSeeBase, session=Depends(get_session)) -> WhatToSee:
    db_whattosee = session.get(WhatToSee, whattosee_id)
    if not db_whattosee:
        raise HTTPException(status_code=404, detail="whattosee not found")

    whattosee_data = whattosee.model_dump(exclude_unset=True)
    for key, value in whattosee_data.items():
        setattr(db_whattosee, key, value)
    session.add(db_whattosee)
    session.commit()
    session.refresh(db_whattosee)
    return db_whattosee


@app.delete("/whattosee/delete/{whattosee_id}")
def whattosee_delete(whattosee_id: int, session=Depends(get_session)):
    whattosee = session.get(WhatToSee, whattosee_id)
    if not whattosee:
        raise HTTPException(status_code=404, detail="whattosee not found")
    session.delete(whattosee)
    session.commit()
    return {"ok": True}


#########################################
# Global environment variables
security = HTTPBearer()
pwd_context = CryptContext(schemes=['bcrypt'])
secret_key = 'supersecret'


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(password, hashed_password):
    return pwd_context.verify(password, hashed_password)


def encode_token(user_id):
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=8),
        'iat': datetime.datetime.utcnow(),
        'sub': user_id
    }
    return jwt.encode(payload, secret_key, algorithm='HS256')


def decode_token(token):
    try:
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        return payload['sub']
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail='Expired signature')
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail='Invalid token')


def auth_wrapper(auth: HTTPAuthorizationCredentials = Security(security)):
    return decode_token(auth.credentials)


def get_current_user(auth: HTTPAuthorizationCredentials = Security(security), session=Depends(get_session)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials'
    )
    username = decode_token(auth.credentials)
    if username is None:
        raise credentials_exception
    user = session.exec(select(User).where(User.username == username)).first()
    if user is None:
        raise credentials_exception
    return user


@app.get("/users/list")
def user_list(session=Depends(get_session)) -> list[User]:
    users = session.query(User).all()
    user_models = [user.model_dump(exclude={'password'}) for user in users]
    return user_models


@app.get("/users/{user_id}")
def user_get(user_id: int, session=Depends(get_session)) -> User:
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.post('/registration', status_code=201, description='Register new user')
def register(user: UserBase, session=Depends(get_session)):
    users = session.exec(select(User)).all()
    if any(x.username == user.username for x in users):
        raise HTTPException(status_code=400, detail='Username is taken')
    hashed_pwd = get_password_hash(user.password)
    user = User(username=user.username, password=hashed_pwd)
    session.add(user)
    session.commit()
    return {"status": 201, "message": "Created"}


@app.post('/login')
def login(user: UserBase, session=Depends(get_session)):
    user_found = session.exec(select(User).where(User.username == user.username)).first()
    if not user_found:
        raise HTTPException(status_code=401, detail='Invalid username and/or password')
    verified = verify_password(user.password, user_found.password)
    if not verified:
        raise HTTPException(status_code=401, detail='Invalid username and/or password')
    token = encode_token(user_found.username)
    return {'token': token}


@app.get('/me', response_model=User)
def get_current_user(user: User = Depends(get_current_user)) -> User:
    return user


if __name__ == '__main__':
    uvicorn.run('main:app', host="localhost", port=8000, reload=True)