from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas, models
from app.database import SessionLocal

router = APIRouter()


# Dependency to get SQLAlchemy session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create a new priority
@router.post("/priorities/", response_model=schemas.Priority)
def create_priority(priority: schemas.PriorityCreate, db: Session = Depends(get_db)):
    db_priority = models.Priority(**priority.dict())
    db.add(db_priority)
    db.commit()
    db.refresh(db_priority)
    return db_priority


# Get priority by ID
@router.get("/priorities/{priority_id}", response_model=schemas.Priority)
def read_priority(priority_id: int, db: Session = Depends(get_db)):
    db_priority = db.query(models.Priority).filter(models.Priority.id == priority_id).first()
    if db_priority is None:
        raise HTTPException(status_code=404, detail="Priority not found")
    return db_priority


# Update priority
@router.put("/priorities/{priority_id}", response_model=schemas.Priority)
def update_priority(priority_id: int, priority: schemas.PriorityCreate, db: Session = Depends(get_db)):
    db_priority = db.query(models.Priority).filter(models.Priority.id == priority_id).first()
    if db_priority is None:
        raise HTTPException(status_code=404, detail="Priority not found")
    for key, value in priority.dict().items():
        setattr(db_priority, key, value)
    db.commit()
    db.refresh(db_priority)
    return db_priority


# Delete priority
@router.delete("/priorities/{priority_id}", response_model=schemas.Priority)
def delete_priority(priority_id: int, db: Session = Depends(get_db)):
    db_priority = db.query(models.Priority).filter(models.Priority.id == priority_id).first()
    if db_priority is None:
        raise HTTPException(status_code=404, detail="Priority not found")
    db.delete(db_priority)
    db.commit()
    return db_priority
