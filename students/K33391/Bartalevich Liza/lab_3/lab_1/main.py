from fastapi import FastAPI
import uvicorn
from fastapi import HTTPException
from fastapi import Depends
from models import (TravelShow, TravelDefault, Travel, 
                    CompanionShow, CompanionDefault, Companion,
                    RegionShow, RegionDefault, Region,
                    LandmarkShow, LandmarkDefault, Landmark,
                    UserShow, UserDefault, User, UserLogin)
from database import init_db, get_session
from typing_extensions import TypedDict
from auth_manager import *

app = FastAPI()


@app.on_event("startup")
def on_startup():
    init_db()


#################################

@app.post("/travel/create")
def travel_create(travel: TravelDefault, session=Depends(get_session)) \
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
def travel_update(travel_id: int, travel: TravelDefault, session=Depends(get_session)) -> Travel:
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


@app.post("companion/create")
def companion_create(companion: CompanionDefault, session=Depends(get_session)) \
        -> TypedDict('Response', {"status": int,
                                  "data": Companion}):
    companion = Companion.model_validate(companion)
    session.add(companion)
    session.commit()
    session.refresh(companion)
    return {"status": 200, "data": companion}


@app.get("companion/list")
def companion_list(session=Depends(get_session)) -> list[Companion]:
    return session.query(Companion).all()


@app.get("/companion/{travel_id}",  response_model=CompanionShow)
def companion_get(travel_id: int, session=Depends(get_session)):
    obj = session.get(Companion, travel_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="travel not found")
    return obj


@app.patch("/companion/update/{travel_id}")
def companion_update(travel_id: int, travel: CompanionDefault, session=Depends(get_session)) -> Companion:
    db_travel = session.get(Companion, travel_id)
    if not db_travel:
        raise HTTPException(status_code=404, detail="travel not found")

    travel_data = travel.model_dump(exclude_unset=True)
    for key, value in travel_data.items():
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
def region_create(region: RegionDefault, session=Depends(get_session)) \
        -> TypedDict('Response', {"status": int,
                                  "data": Region}):
    region = Region.model_validate(region)
    session.add(Region)
    session.commit()
    session.refresh(Region)
    return {"status": 200, "data": region}


@app.get("/region/list")
def regions_list(session=Depends(get_session)) -> list[Region]:
    return session.query(Region).all()


@app.get("/region/{region_id}",  response_model=RegionShow)
def region_get(region_id: int, session=Depends(get_session)):
    obj = session.get(Region, region_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="Region not found")
    return obj


@app.patch("/region/update/{region_id}")
def Region_update(region_id: int, Region: RegionDefault, session=Depends(get_session)) -> Region:
    db_region = session.get(Region, region_id)
    if not db_region:
        raise HTTPException(status_code=404, detail="Region not found")

    region_data = Region.model_dump(exclude_unset=True)
    for key, value in region_data.items():
        setattr(db_region, key, value)
    session.add(db_region)
    session.commit()
    session.refresh(db_region)
    return db_region


@app.delete("/region/delete/{region_id}")
def Region_delete(region_id: int, session=Depends(get_session)):
    region = session.get(Region, region_id)
    if not Region:
        raise HTTPException(status_code=404, detail="Region not found")
    session.delete(Region)
    session.commit()
    return {"ok": True}


@app.post("/landmark/create")
def landmark_create(landmark: LandmarkDefault, session=Depends(get_session)) \
        -> TypedDict('Response', {"status": int,
                                  "data": Landmark}):
    landmark = Landmark.model_validate(landmark)
    session.add(landmark)
    session.commit()
    session.refresh(landmark)
    return {"status": 200, "data": landmark}


@app.get("/list-landmarks-in-region/{region_id}")
def landmarks_list(region_id: int, session=Depends(get_session)) -> list[Landmark]:
    return session.query(Landmark).filter(Landmark.Region_id == region_id).all()


@app.get("/landmark/{landmark_id}",  response_model=LandmarkShow)
def landmark_get(landmark_id: int, session=Depends(get_session)):
    obj = session.get(Landmark, landmark_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="sublandmark not found")
    return obj


@app.patch("/landmark/update/{landmark_id}")
def landmark_update(landmark_id: int, landmark: LandmarkDefault, session=Depends(get_session)) -> Landmark:
    db_landmark = session.get(Landmark, landmark_id)
    if not db_landmark:
        raise HTTPException(status_code=404, detail="landmark not found")

    landmark_data = landmark.model_dump(exclude_unset=True)
    for key, value in landmark_data.items():
        setattr(db_landmark, key, value)
    session.add(db_landmark)
    session.commit()
    session.refresh(db_landmark)
    return db_landmark


@app.delete("/landmark/delete/{landmark_id}")
def landmark_delete(landmark_id: int, session=Depends(get_session)):
    landmark = session.get(Landmark, landmark_id)
    if not landmark:
        raise HTTPException(status_code=404, detail="landmark not found")
    session.delete(landmark)
    session.commit()
    return {"ok": True}


#########################################

@app.get("/users/list")
def user_list(session=Depends(get_session)) -> list[User]:
    users = session.query(User).all()
    user_models = [user.model_dump(exclude={'password'}) for user in users]
    return user_models


@app.get("/users/{user_id}")
def user_get(user_id: int, session=Depends(get_session)) -> UserShow:
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.post("/users/", response_model=User)
def create_user(user: UserDefault, session: Session = Depends(get_session)):
    db_user = User(
        username=user.username,
        email=user.email,
        password=get_password_hash(user.password),
        description=user.description,
        work=user.work
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@app.post("/token")
async def login_for_access_token(
    form_data: UserLogin = Depends(),
    session: Session = Depends(get_session),
):
    user = authenticate_user(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

if __name__ == '__main__':
    uvicorn.run('main:app', host="localhost", port=8000, reload=True)