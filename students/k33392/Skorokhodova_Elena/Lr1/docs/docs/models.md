#Модели

Определение структуры бд с помощью 
SQLAlchemy, представленную в виде классов Python.
Реализованы классы: User, UserProfile, Trip, UserTrip, TripReview.

    from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Float
        from sqlalchemy.orm import relationship
        from sqlalchemy.ext.declarative import declarative_base
        from datetime import datetime
    
    Base = declarative_base()
    
    
    class User(Base):
        __tablename__ = "users"
    
        id = Column(Integer, primary_key=True, index=True)
        username = Column(String, unique=True, index=True)
        email = Column(String, unique=True, index=True)
        hashed_password = Column(String)
        is_active = Column(Boolean, default=True)
    
        profile = relationship("UserProfile", back_populates="user")
        trips = relationship("Trip", back_populates="owner")
    
    
    class UserProfile(Base):
        __tablename__ = "user_profiles"
    
        id = Column(Integer, primary_key=True, index=True)
        user_id = Column(Integer, ForeignKey("users.id"))
        username = Column(String)
        skills = Column(String)
        experience = Column(String)
        preferences = Column(String)
        user = relationship("User", back_populates="profile")
    
    
    class Trip(Base):
        __tablename__ = "trips"
    
        id = Column(Integer, primary_key=True, index=True)
        owner_id = Column(Integer, ForeignKey("users.id"))
        departure_location = Column(String)
        destination = Column(String)
        start_date = Column(DateTime)
        end_date = Column(DateTime)
        duration = Column(Integer)
        details = Column(String)
    
        owner = relationship("User", back_populates="trips")
        users = relationship("User", secondary="user_trips", back_populates="trips")
        reviews = relationship("TripReview", back_populates="trip")
    
    
    class UserTrip(Base):
        __tablename__ = "user_trips"
    
        id = Column(Integer, primary_key=True, index=True)
        user_id = Column(Integer, ForeignKey("users.id"))
        trip_id = Column(Integer, ForeignKey("trips.id"))
        role = Column(String)
    
    
    class TripReview(Base):
        __tablename__ = "trip_reviews"
    
        id = Column(Integer, primary_key=True, index=True)
        trip_id = Column(Integer, ForeignKey("trips.id"))
        user_id = Column(Integer, ForeignKey("users.id"))
        rating = Column(Integer)
        comment = Column(String)
    
        user = relationship("User")
        trip = relationship("Trip", back_populates="reviews")
