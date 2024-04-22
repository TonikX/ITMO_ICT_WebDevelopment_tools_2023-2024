from datetime import datetime

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from travel_app import crud, schemas, database

app = FastAPI()


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/register/", response_model=schemas.User)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    return crud.create_user(db=db, user=user)


@app.post("/login/")
def login_user(username: str, password: str, db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, username=username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.password != password:
        raise HTTPException(status_code=401, detail="Incorrect password")

    return {"message": "Login successful"}


@app.post("/user_profiles/", response_model=schemas.UserProfile)
def create_user_profile(user_profile: schemas.UserProfileCreate, db: Session = Depends(get_db)):
    return crud.create_user_profile(db=db, user_profile=user_profile)


@app.get("/user_profiles/{user_profile_id}", response_model=schemas.UserProfile)
def read_user_profile(user_profile_id: int, db: Session = Depends(get_db)):
    db_user_profile = crud.get_user_profile(db, user_profile_id=user_profile_id)
    if db_user_profile is None:
        raise HTTPException(status_code=404, detail="User profile not found")

    db_user_profile.user = crud.get_user(db, user_id=db_user_profile.user_id)  # вложенность для профиля пользователя

    return db_user_profile


@app.put("/user_profiles/{user_profile_id}", response_model=schemas.UserProfile)
def update_user_profile(user_profile_id: int, user_profile: schemas.UserProfileUpdate, db: Session = Depends(get_db)):
    db_user_profile = crud.update_user_profile(db, user_profile_id=user_profile_id, user_profile_data=user_profile)
    if db_user_profile is None:
        raise HTTPException(status_code=404, detail="User profile not found")
    return db_user_profile


@app.delete("/user_profiles/{user_profile_id}")
def delete_user_profile(user_profile_id: int, db: Session = Depends(get_db)):
    db_user_profile = crud.delete_user_profile(db, user_profile_id=user_profile_id)
    if db_user_profile is None:
        raise HTTPException(status_code=404, detail="User profile not found")
    return {"message": "User profile deleted successfully"}


@app.post("/trips/", response_model=schemas.Trip)
def create_trip(trip: schemas.TripCreate, db: Session = Depends(get_db)):
    return crud.create_trip(db=db, trip=trip)


@app.get("/trips/{trip_id}", response_model=schemas.Trip)
def read_trip(trip_id: int, db: Session = Depends(get_db)):
    db_trip = crud.get_trip(db, trip_id=trip_id)
    if db_trip is None:
        raise HTTPException(status_code=404, detail="Trip not found")

    db_trip.owner = crud.get_user(db, user_id=db_trip.owner_id)  # вложенность для владельца путешествия

    return db_trip


@app.put("/trips/{trip_id}", response_model=schemas.Trip)
def update_trip(trip_id: int, trip: schemas.TripUpdate, db: Session = Depends(get_db)):
    db_trip = crud.update_trip(db, trip_id=trip_id, trip_data=trip)
    if db_trip is None:
        raise HTTPException(status_code=404, detail="Trip not found")
    return db_trip


@app.delete("/trips/{trip_id}")
def delete_trip(trip_id: int, db: Session = Depends(get_db)):
    db_trip = crud.delete_trip(db, trip_id=trip_id)
    if db_trip is None:
        raise HTTPException(status_code=404, detail="Trip not found")
    return {"message": "Trip deleted successfully"}


@app.post("/user_trips/", response_model=schemas.UserTrip)
def create_user_trip(user_trip: schemas.UserTripCreate, db: Session = Depends(get_db)):
    return crud.create_user_trip(db=db, user_trip=user_trip)


@app.delete("/user_trips/{user_id}/{trip_id}")
def delete_user_trip(user_id: int, trip_id: int, db: Session = Depends(get_db)):
    db_user_trip = crud.delete_user_trip(db, user_id=user_id, trip_id=trip_id)
    if db_user_trip is None:
        raise HTTPException(status_code=404, detail="User trip not found")
    return {"message": "User trip deleted successfully"}


@app.post("/trip_reviews/", response_model=schemas.TripReview)
def create_trip_review(trip_review: schemas.TripReviewCreate, db: Session = Depends(get_db)):
    return crud.create_trip_review(db=db, trip_review=trip_review)


@app.delete("/trip_reviews/{trip_review_id}")
def delete_trip_review(trip_review_id: int, db: Session = Depends(get_db)):
    db_trip_review = crud.delete_trip_review(db, trip_review_id=trip_review_id)
    if db_trip_review is None:
        raise HTTPException(status_code=404, detail="Trip review not found")
    return {"message": "Trip review deleted successfully"}


@app.get("/companions/")
async def search_companions(departure_location: str, destination: str, start_date: datetime, end_date: datetime,
                            db: Session = Depends(get_db)):
    companions = crud.search_companions(db, departure_location, destination, start_date, end_date)
    if not companions:
        raise HTTPException(status_code=404, detail="No companions found")

    for companion in companions:
        companion.profile = crud.get_user_profile(db,
                                                  user_profile_id=companion.profile_id)  # вложенность для профилей компаньонов

    return companions


