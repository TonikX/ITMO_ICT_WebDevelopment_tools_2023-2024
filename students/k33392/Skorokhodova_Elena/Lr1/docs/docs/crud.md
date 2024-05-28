#Функции CRUD-операций

Здесь представлена реализация функций для CRUD-операций приложения, таких как
создание объекта, редактирование, удаление, получение.

    from datetime import datetime

    from passlib.context import CryptContext
    from sqlalchemy.orm import Session, joinedload
    from . import models, schemas
    
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    
    def get_user_by_username(db: Session, username: str):
        return db.query(models.User).filter(models.User.username == username).first()
    
    
    def create_user(db: Session, user: schemas.UserCreate):
        hashed_password = pwd_context.hash(user.password)
        db_user = models.User(username=user.username, email=user.email, hashed_password=hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    
    
    def get_user(db: Session, user_id: int):
        return db.query(models.User).filter(models.User.id == user_id).first()
    
    
    def create_user_profile(db: Session, user_profile: schemas.UserProfileCreate):
        db_user_profile = models.UserProfile(**user_profile.dict())
        db.add(db_user_profile)
        db.commit()
        db.refresh(db_user_profile)
        return db_user_profile
    
    
    def get_user_profile(db: Session, user_profile_id: int):
        return db.query(models.UserProfile).filter(models.UserProfile.id == user_profile_id).first()
    
    
    def get_user_by_email(db: Session, email: str):
        return db.query(models.User).filter(models.User.email == email).first()
    
    
    def update_user_profile(db: Session, user_profile_id: int, user_profile_data: schemas.UserProfileUpdate):
        db_user_profile = db.query(models.UserProfile).filter(models.UserProfile.id == user_profile_id).first()
        if db_user_profile:
            for key, value in user_profile_data.dict().items():
                setattr(db_user_profile, key, value)
            db.commit()
            db.refresh(db_user_profile)
        return db_user_profile
    
    
    def delete_user_profile(db: Session, user_profile_id: int):
        db_user_profile = db.query(models.UserProfile).filter(models.UserProfile.id == user_profile_id).first()
        if db_user_profile:
            db.delete(db_user_profile)
            db.commit()
        return db_user_profile
    
    
    def create_trip(db: Session, trip: schemas.TripCreate):
        db_trip = models.Trip(**trip.dict())
        db.add(db_trip)
        db.commit()
        db.refresh(db_trip)
        return db_trip
    
    
    def get_trip(db: Session, trip_id: int):
        return db.query(models.Trip).filter(models.Trip.id == trip_id).first()
    
    
    def update_trip(db: Session, trip_id: int, trip_data: schemas.TripUpdate):
        db_trip = db.query(models.Trip).filter(models.Trip.id == trip_id).first()
        if db_trip:
            for key, value in trip_data.dict().items():
                setattr(db_trip, key, value)
            db.commit()
            db.refresh(db_trip)
        return db_trip
    
    
    def delete_trip(db: Session, trip_id: int):
        db_trip = db.query(models.Trip).filter(models.Trip.id == trip_id).first()
        if db_trip:
            db.delete(db_trip)
            db.commit()
        return db_trip
    
    
    def create_user_trip(db: Session, user_trip: schemas.UserTripCreate):
        db_user_trip = models.UserTrip(**user_trip.dict())
        db.add(db_user_trip)
        db.commit()
        db.refresh(db_user_trip)
        return db_user_trip
    
    
    def delete_user_trip(db: Session, user_id: int, trip_id: int):
        db_user_trip = db.query(models.UserTrip).filter(models.UserTrip.user_id == user_id,
                                                        models.UserTrip.trip_id == trip_id).first()
        if db_user_trip:
            db.delete(db_user_trip)
            db.commit()
        return db_user_trip
    
    
    def create_trip_review(db: Session, trip_review: schemas.TripReviewCreate):
        db_trip_review = models.TripReview(**trip_review.dict())
        db.add(db_trip_review)
        db.commit()
        db.refresh(db_trip_review)
        return db_trip_review
    
    
    def delete_trip_review(db: Session, trip_review_id: int):
        db_trip_review = db.query(models.TripReview).filter(models.TripReview.id == trip_review_id).first()
        if db_trip_review:
            db.delete(db_trip_review)
            db.commit()
        return db_trip_review
    
    
    def search_companions(db: Session, departure_location: str, destination: str, start_date: datetime, end_date: datetime):
        companions = db.query(models.User).join(models.Trip).filter(
            models.Trip.departure_location == departure_location,
            models.Trip.destination == destination,
            models.Trip.start_date >= start_date,
            models.Trip.end_date <= end_date
        ).options(joinedload(models.User.profile)).all()
        return companions



