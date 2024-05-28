#Cхемы

Схемы данных с использованием Pydantic, 
которые используются для валидации и 
сериализации данных в приложении.

    from datetime import datetime
    
    from pydantic import BaseModel
    from typing import List, Optional
    
    
    class UserCreate(BaseModel):
        username: str
        email: str
        password: str
    
    
    class User(BaseModel):
        id: int
        username: str
        email: str
    
        class Config:
            orm_mode = True
    
    
    class UserProfileBase(BaseModel):
        user_id: int
        username: str
        email: str
        skills: str
        experience: str
        preferences: str
    
    
    class UserProfileCreate(UserProfileBase):
        pass
    
    
    class UserProfileUpdate(UserProfileBase):
        pass
    
    
    class UserProfile(UserProfileBase):
        id: int
    
        class Config:
            orm_mode = True
    
    
    class TripBase(BaseModel):
        departure_location: str
        destination: str
        start_date: datetime
        end_date: datetime
        duration: int
        details: Optional[str] = None
    
    
    class TripCreate(TripBase):
        pass
    
    
    class TripUpdate(TripBase):
        pass
    
    
    class Trip(TripBase):
        id: int
    
        class Config:
            orm_mode = True
    
    
    class UserTripBase(BaseModel):
        user_id: int
        trip_id: int
        role: Optional[str] = None
    
    
    class UserTripCreate(UserTripBase):
        pass
    
    
    class UserTrip(UserTripBase):
        id: int
    
        class Config:
            orm_mode = True
    
    
    class TripReviewBase(BaseModel):
        trip_id: int
        user_id: int
        rating: int
        comment: Optional[str] = None
    
    
    class TripReviewCreate(TripReviewBase):
        pass
    
    
    class TripReview(TripReviewBase):
        id: int
    
        class Config:
            orm_mode = True
